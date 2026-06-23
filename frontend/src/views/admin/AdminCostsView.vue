<template>
  <div class="page">
    <RouterLink to="/admin" class="back-link">← Admin console</RouterLink>

    <header class="admin-page-header">
      <div>
        <h1 class="page-title">Costs</h1>
        <p class="page-subtitle">{{ items.length }} cost entries · {{ formatCurrency(totalCost) }} total</p>
      </div>
      <button class="btn btn-primary" @click="openCreate">+ New cost</button>
    </header>

    <div v-if="error" class="alert alert-error" style="margin-bottom: 1.25rem">{{ error }}</div>

    <div class="toolbar card">
      <input v-model="search" class="input toolbar__search" type="search" placeholder="Search costs…" />
      <select v-model="categoryFilter" class="select toolbar__select">
        <option value="all">All categories</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ labelize(cat) }}</option>
      </select>
    </div>

    <div v-if="loading" class="state card"><span class="spinner" /><p>Loading…</p></div>
    <div v-else-if="filtered.length === 0" class="state card"><p>No costs found.</p></div>

    <div v-else class="card table-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Lift</th>
            <th>Category</th>
            <th>Description</th>
            <th class="text-right">Amount</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in filtered" :key="c.id">
            <td class="cell-muted">{{ formatDate(c.incurred_on) }}</td>
            <td>
              <div class="cell-strong">{{ c.lift_name }}</div>
              <div class="mono cell-muted" style="font-size: 0.78rem">{{ c.lift_uid }}</div>
            </td>
            <td><span class="badge" :class="costCategoryBadge(c.category)">{{ labelize(c.category) }}</span></td>
            <td class="cell-muted">{{ c.description || '—' }}</td>
            <td class="cell-num cell-strong">{{ formatCurrency(c.amount) }}</td>
            <td class="text-right">
              <button class="btn btn-subtle btn-sm" @click="remove(c)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <AppModal v-if="showCreate" title="New cost entry" @close="showCreate = false">
      <div v-if="formError" class="alert alert-error" style="margin-bottom: 1rem">{{ formError }}</div>
      <form @submit.prevent="submit">
        <div class="form-grid">
          <div class="field col-span-2">
            <label class="label">Lift</label>
            <select v-model.number="form.lift_id" class="select" required>
              <option :value="0" disabled>Select a lift…</option>
              <option v-for="l in lifts" :key="l.id" :value="l.id">
                {{ l.name }} ({{ l.uid }})
              </option>
            </select>
          </div>
          <div class="field">
            <label class="label">Category</label>
            <select v-model="form.category" class="select">
              <option v-for="cat in categories" :key="cat" :value="cat">{{ labelize(cat) }}</option>
            </select>
          </div>
          <div class="field">
            <label class="label">Amount</label>
            <input v-model.number="form.amount" class="input" type="number" min="0" step="1" required />
          </div>
          <div class="field">
            <label class="label">Date</label>
            <input v-model="form.incurred_on" class="input" type="date" required />
          </div>
          <div class="field col-span-2">
            <label class="label">Description</label>
            <input v-model="form.description" class="input" />
          </div>
        </div>
        <div class="modal__actions">
          <button type="button" class="btn btn-secondary" @click="showCreate = false">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            <span v-if="saving" class="spinner btn-spinner" />
            {{ saving ? 'Saving…' : 'Add cost' }}
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
import { createCost, deleteCost, fetchCosts } from '../../api/costs'
import { fetchLifts } from '../../api/lifts'
import type { Cost, CostCreate } from '../../types/cost'
import type { Lift } from '../../types/lift'
import { costCategoryBadge, extractApiError, formatCurrency, formatDate } from '../../utils/format'

const categories = ['maintenance', 'repair', 'insurance', 'transport', 'other']

const items = ref<Cost[]>([])
const lifts = ref<Lift[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const search = ref('')
const categoryFilter = ref('all')

const showCreate = ref(false)
const saving = ref(false)
const formError = ref<string | null>(null)

function blankForm(): CostCreate {
  return {
    lift_id: 0,
    category: 'maintenance',
    description: '',
    amount: 0,
    incurred_on: new Date().toISOString().slice(0, 10),
  }
}
const form = reactive<CostCreate>(blankForm())

const totalCost = computed(() => items.value.reduce((sum, c) => sum + c.amount, 0))

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  return items.value.filter((c) => {
    if (categoryFilter.value !== 'all' && c.category !== categoryFilter.value) return false
    if (
      q &&
      !(c.lift_name ?? '').toLowerCase().includes(q) &&
      !(c.description ?? '').toLowerCase().includes(q)
    ) {
      return false
    }
    return true
  })
})

function labelize(value: string): string {
  return value.charAt(0).toUpperCase() + value.slice(1)
}

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    const [costList, liftList] = await Promise.all([fetchCosts(), fetchLifts()])
    items.value = costList
    lifts.value = liftList
  } catch (e) {
    error.value = extractApiError(e, 'Failed to load costs.')
  } finally {
    loading.value = false
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
    const created = await createCost({ ...form })
    items.value.unshift(created)
    showCreate.value = false
  } catch (e) {
    formError.value = extractApiError(e, 'Failed to create cost.')
  } finally {
    saving.value = false
  }
}

async function remove(c: Cost): Promise<void> {
  if (!window.confirm('Delete this cost entry?')) return
  error.value = null
  try {
    await deleteCost(c.id)
    items.value = items.value.filter((x) => x.id !== c.id)
  } catch (e) {
    error.value = extractApiError(e, 'Failed to delete cost.')
  }
}

onMounted(load)
</script>
