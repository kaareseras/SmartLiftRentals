<template>
  <div class="page">
    <RouterLink to="/admin" class="back-link">← Admin console</RouterLink>

    <header class="admin-page-header">
      <div>
        <h1 class="page-title">Customers</h1>
        <p class="page-subtitle">{{ items.length }} customers</p>
      </div>
      <button class="btn btn-primary" @click="openCreate">+ New customer</button>
    </header>

    <div v-if="error" class="alert alert-error" style="margin-bottom: 1.25rem">{{ error }}</div>

    <div class="toolbar card">
      <input v-model="search" class="input toolbar__search" type="search" placeholder="Search customers…" />
    </div>

    <div v-if="loading" class="state card"><span class="spinner" /><p>Loading…</p></div>
    <div v-else-if="filtered.length === 0" class="state card"><p>No customers found.</p></div>

    <div v-else class="card table-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Company</th>
            <th>Email</th>
            <th>Phone</th>
            <th class="text-right">Contracts</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in filtered" :key="c.id">
            <td>
              <div class="cell-avatar">
                <span class="cell-avatar__img">{{ initialsOf(c.name) }}</span>
                <span class="cell-strong">{{ c.name }}</span>
              </div>
            </td>
            <td class="cell-muted">{{ c.company || '—' }}</td>
            <td class="cell-muted">{{ c.email || '—' }}</td>
            <td class="cell-muted">{{ c.phone || '—' }}</td>
            <td class="cell-num">{{ c.contract_count }}</td>
            <td class="text-right">
              <button class="btn btn-subtle btn-sm" @click="remove(c)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <AppModal v-if="showCreate" title="New customer" @close="showCreate = false">
      <div v-if="formError" class="alert alert-error" style="margin-bottom: 1rem">{{ formError }}</div>
      <form @submit.prevent="submit">
        <div class="form-grid">
          <div class="field">
            <label class="label">Name</label>
            <input v-model="form.name" class="input" required />
          </div>
          <div class="field">
            <label class="label">Company</label>
            <input v-model="form.company" class="input" />
          </div>
          <div class="field">
            <label class="label">Email</label>
            <input v-model="form.email" class="input" type="email" />
          </div>
          <div class="field">
            <label class="label">Phone</label>
            <input v-model="form.phone" class="input" />
          </div>
          <div class="field col-span-2">
            <label class="label">Address</label>
            <input v-model="form.address" class="input" />
          </div>
        </div>
        <div class="modal__actions">
          <button type="button" class="btn btn-secondary" @click="showCreate = false">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            <span v-if="saving" class="spinner btn-spinner" />
            {{ saving ? 'Saving…' : 'Create customer' }}
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
import { createCustomer, deleteCustomer, fetchCustomers } from '../../api/customers'
import type { Customer, CustomerCreate } from '../../types/customer'
import { extractApiError, initialsOf } from '../../utils/format'

const items = ref<Customer[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const search = ref('')

const showCreate = ref(false)
const saving = ref(false)
const formError = ref<string | null>(null)
const form = reactive<CustomerCreate>({ name: '', company: '', email: '', phone: '', address: '' })

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return items.value
  return items.value.filter(
    (c) =>
      c.name.toLowerCase().includes(q) ||
      (c.company ?? '').toLowerCase().includes(q) ||
      (c.email ?? '').toLowerCase().includes(q),
  )
})

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    items.value = await fetchCustomers()
  } catch (e) {
    error.value = extractApiError(e, 'Failed to load customers.')
  } finally {
    loading.value = false
  }
}

function openCreate(): void {
  form.name = ''
  form.company = ''
  form.email = ''
  form.phone = ''
  form.address = ''
  formError.value = null
  showCreate.value = true
}

async function submit(): Promise<void> {
  saving.value = true
  formError.value = null
  try {
    const created = await createCustomer({ ...form })
    items.value.push(created)
    items.value.sort((a, b) => a.name.localeCompare(b.name))
    showCreate.value = false
  } catch (e) {
    formError.value = extractApiError(e, 'Failed to create customer.')
  } finally {
    saving.value = false
  }
}

async function remove(c: Customer): Promise<void> {
  if (!window.confirm(`Delete customer “${c.name}”? This also removes their contracts.`)) return
  error.value = null
  try {
    await deleteCustomer(c.id)
    items.value = items.value.filter((x) => x.id !== c.id)
  } catch (e) {
    error.value = extractApiError(e, 'Failed to delete customer.')
  }
}

onMounted(load)
</script>

<style scoped>
.cell-avatar {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.cell-avatar__img {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--color-primary-soft);
  color: var(--color-primary-pressed);
  font-weight: 700;
  font-size: 0.72rem;
  flex-shrink: 0;
}
</style>
