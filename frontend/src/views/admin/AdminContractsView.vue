<template>
  <div class="page">
    <RouterLink to="/admin" class="back-link">← Admin console</RouterLink>

    <header class="admin-page-header">
      <div>
        <h1 class="page-title">Contracts</h1>
        <p class="page-subtitle">{{ items.length }} rental contracts</p>
      </div>
      <button class="btn btn-primary" @click="openCreate">+ New rental</button>
    </header>

    <div v-if="error" class="alert alert-error" style="margin-bottom: 1.25rem">{{ error }}</div>

    <div class="toolbar card">
      <input v-model="search" class="input toolbar__search" type="search" placeholder="Search by lift or customer…" />
      <select v-model="statusFilter" class="select toolbar__select">
        <option value="all">All statuses</option>
        <option value="active">Active</option>
        <option value="completed">Completed</option>
        <option value="cancelled">Cancelled</option>
      </select>
    </div>

    <div v-if="loading" class="state card"><span class="spinner" /><p>Loading…</p></div>
    <div v-else-if="filtered.length === 0" class="state card"><p>No contracts found.</p></div>

    <div v-else class="card table-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Lift</th>
            <th>Customer</th>
            <th>Start</th>
            <th>End</th>
            <th class="text-right">Days</th>
            <th class="text-right">Day rate</th>
            <th class="text-right">Total</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in filtered" :key="c.id">
            <td>
              <div class="cell-strong">{{ c.lift_name }}</div>
              <div class="mono cell-muted" style="font-size: 0.78rem">{{ c.lift_uid }}</div>
            </td>
            <td>{{ c.customer_name }}</td>
            <td class="cell-muted">{{ formatDate(c.start_date) }}</td>
            <td class="cell-muted">{{ formatDate(c.end_date) }}</td>
            <td class="cell-num">{{ c.duration_days }}</td>
            <td class="cell-num">{{ formatCurrency(c.daily_rate) }}</td>
            <td class="cell-num cell-strong">{{ formatCurrency(c.total_price) }}</td>
            <td><span class="badge" :class="contractStatusBadge(c.status)">{{ c.status }}</span></td>
            <td class="text-right">
              <button class="btn btn-subtle btn-sm" @click="remove(c)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <AppModal v-if="showCreate" title="New rental contract" @close="showCreate = false">
      <div v-if="formError" class="alert alert-error" style="margin-bottom: 1rem">{{ formError }}</div>
      <form @submit.prevent="submit">
        <div class="form-grid">
          <div class="field col-span-2">
            <label class="label">Lift</label>
            <select v-model.number="form.lift_id" class="select" required @change="prefillRate">
              <option :value="0" disabled>Select a lift…</option>
              <option v-for="l in lifts" :key="l.id" :value="l.id">
                {{ l.name }} ({{ l.uid }}) — {{ l.lift_type_name }}
              </option>
            </select>
          </div>
          <div class="field col-span-2">
            <label class="label">Customer</label>
            <select v-model.number="form.customer_id" class="select" required>
              <option :value="0" disabled>Select a customer…</option>
              <option v-for="c in customers" :key="c.id" :value="c.id">
                {{ c.name }}{{ c.company ? ` — ${c.company}` : '' }}
              </option>
            </select>
          </div>
          <div class="field">
            <label class="label">Start date</label>
            <input v-model="form.start_date" class="input" type="date" required />
          </div>
          <div class="field">
            <label class="label">Duration (days)</label>
            <input v-model.number="form.duration_days" class="input" type="number" min="1" required />
          </div>
          <div class="field">
            <label class="label">Daily rate</label>
            <input v-model.number="form.daily_rate" class="input" type="number" min="0" step="1" required />
          </div>
          <div class="field">
            <label class="label">Status</label>
            <select v-model="form.status" class="select">
              <option value="active">Active</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          <div class="field col-span-2">
            <label class="label">Notes</label>
            <textarea v-model="form.notes" class="input" rows="2" />
          </div>
        </div>

        <div class="contract-total">
          <span>Estimated total</span>
          <strong>{{ formatCurrency(estimatedTotal) }}</strong>
        </div>

        <div class="modal__actions">
          <button type="button" class="btn btn-secondary" @click="showCreate = false">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            <span v-if="saving" class="spinner btn-spinner" />
            {{ saving ? 'Saving…' : 'Create rental' }}
          </button>
        </div>
      </form>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { RouterLink } from 'vue-router'

import AppModal from '../../components/AppModal.vue'
import { createContract, deleteContract, fetchContracts } from '../../api/contracts'
import { fetchLifts } from '../../api/lifts'
import { fetchCustomers } from '../../api/customers'
import type { Contract, ContractCreate } from '../../types/contract'
import type { Lift } from '../../types/lift'
import type { Customer } from '../../types/customer'
import { contractStatusBadge, extractApiError, formatCurrency, formatDate } from '../../utils/format'

const items = ref<Contract[]>([])
const lifts = ref<Lift[]>([])
const customers = ref<Customer[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const search = ref('')
const statusFilter = ref<'all' | 'active' | 'completed' | 'cancelled'>('all')

const showCreate = ref(false)
const saving = ref(false)
const formError = ref<string | null>(null)

function blankForm(): ContractCreate {
  return {
    lift_id: 0,
    customer_id: 0,
    start_date: new Date().toISOString().slice(0, 10),
    duration_days: 30,
    daily_rate: 0,
    status: 'active',
    notes: '',
  }
}
const form = reactive<ContractCreate>(blankForm())

const estimatedTotal = computed(() => (form.daily_rate || 0) * (form.duration_days || 0))

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  return items.value.filter((c) => {
    if (statusFilter.value !== 'all' && c.status !== statusFilter.value) return false
    if (
      q &&
      !(c.lift_name ?? '').toLowerCase().includes(q) &&
      !(c.customer_name ?? '').toLowerCase().includes(q) &&
      !(c.lift_uid ?? '').toLowerCase().includes(q)
    ) {
      return false
    }
    return true
  })
})

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    const [contractList, liftList, customerList] = await Promise.all([
      fetchContracts(),
      fetchLifts(),
      fetchCustomers(),
    ])
    items.value = contractList
    lifts.value = liftList
    customers.value = customerList
  } catch (e) {
    error.value = extractApiError(e, 'Failed to load contracts.')
  } finally {
    loading.value = false
  }
}

function prefillRate(): void {
  const lift = lifts.value.find((l) => l.id === form.lift_id)
  const rate = lift?.lift_type?.default_daily_rate
  if (rate != null && !form.daily_rate) {
    form.daily_rate = rate
  }
}

function openCreate(): void {
  Object.assign(form, blankForm())
  formError.value = null
  showCreate.value = true
}

async function submit(): Promise<void> {
  saving.value = true
  formError.value = null
  try {
    const created = await createContract({ ...form })
    items.value.unshift(created)
    showCreate.value = false
    await refreshReferences()
  } catch (e) {
    formError.value = extractApiError(e, 'Failed to create contract.')
  } finally {
    saving.value = false
  }
}

async function refreshReferences(): Promise<void> {
  try {
    customers.value = await fetchCustomers()
  } catch {
    // non-critical
  }
}

async function remove(c: Contract): Promise<void> {
  if (!window.confirm(`Delete the contract for ${c.lift_name} → ${c.customer_name}?`)) return
  error.value = null
  try {
    await deleteContract(c.id)
    items.value = items.value.filter((x) => x.id !== c.id)
  } catch (e) {
    error.value = extractApiError(e, 'Failed to delete contract.')
  }
}

onMounted(load)
</script>

<style scoped>
.contract-total {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1rem;
  padding: 0.85rem 1rem;
  border-radius: var(--radius-md);
  background: var(--color-primary-tint);
  border: 1px solid var(--color-border);
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.contract-total strong {
  font-size: 1.25rem;
  color: var(--color-primary-pressed);
}
</style>
