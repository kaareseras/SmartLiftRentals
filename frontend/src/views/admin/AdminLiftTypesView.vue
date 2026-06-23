<template>
  <div class="page">
    <RouterLink to="/admin" class="back-link">← Admin console</RouterLink>

    <header class="admin-page-header">
      <div>
        <h1 class="page-title">Lift types</h1>
        <p class="page-subtitle">{{ items.length }} types in the catalogue</p>
      </div>
      <button class="btn btn-primary" @click="openCreate">+ New lift type</button>
    </header>

    <div v-if="error" class="alert alert-error" style="margin-bottom: 1.25rem">{{ error }}</div>

    <div class="toolbar card">
      <input v-model="search" class="input toolbar__search" type="search" placeholder="Search types…" />
    </div>

    <div v-if="loading" class="state card"><span class="spinner" /><p>Loading…</p></div>
    <div v-else-if="filtered.length === 0" class="state card"><p>No lift types found.</p></div>

    <div v-else class="card table-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Manufacturer</th>
            <th>Model</th>
            <th class="text-right">Default day rate</th>
            <th class="text-right">Lifts</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in filtered" :key="t.id">
            <td class="cell-strong">{{ t.name }}</td>
            <td class="cell-muted">{{ t.manufacturer || '—' }}</td>
            <td class="mono">{{ t.model }}</td>
            <td class="cell-num">{{ t.default_daily_rate != null ? formatCurrency(t.default_daily_rate) : '—' }}</td>
            <td class="cell-num">{{ t.lift_count }}</td>
            <td class="text-right">
              <button class="btn btn-subtle btn-sm" @click="remove(t)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <AppModal v-if="showCreate" title="New lift type" @close="showCreate = false">
      <div v-if="formError" class="alert alert-error" style="margin-bottom: 1rem">{{ formError }}</div>
      <form @submit.prevent="submit">
        <div class="form-grid">
          <div class="field">
            <label class="label">Name</label>
            <input v-model="form.name" class="input" required />
          </div>
          <div class="field">
            <label class="label">Model</label>
            <input v-model="form.model" class="input" required />
          </div>
          <div class="field">
            <label class="label">Manufacturer</label>
            <input v-model="form.manufacturer" class="input" />
          </div>
          <div class="field">
            <label class="label">Default day rate</label>
            <input v-model.number="form.default_daily_rate" class="input" type="number" min="0" step="1" />
          </div>
          <div class="field col-span-2">
            <label class="label">Description</label>
            <textarea v-model="form.description" class="input" rows="3" />
          </div>
        </div>
        <div class="modal__actions">
          <button type="button" class="btn btn-secondary" @click="showCreate = false">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            <span v-if="saving" class="spinner btn-spinner" />
            {{ saving ? 'Saving…' : 'Create type' }}
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
import {
  createLiftType,
  deleteLiftType,
  fetchLiftTypes,
} from '../../api/liftTypes'
import type { LiftType, LiftTypeCreate } from '../../types/liftType'
import { extractApiError, formatCurrency } from '../../utils/format'

const items = ref<LiftType[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const search = ref('')

const showCreate = ref(false)
const saving = ref(false)
const formError = ref<string | null>(null)
const form = reactive<LiftTypeCreate>({
  name: '',
  model: '',
  manufacturer: '',
  description: '',
  default_daily_rate: null,
})

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return items.value
  return items.value.filter(
    (t) =>
      t.name.toLowerCase().includes(q) ||
      t.model.toLowerCase().includes(q) ||
      (t.manufacturer ?? '').toLowerCase().includes(q),
  )
})

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    items.value = await fetchLiftTypes()
  } catch (e) {
    error.value = extractApiError(e, 'Failed to load lift types.')
  } finally {
    loading.value = false
  }
}

function openCreate(): void {
  form.name = ''
  form.model = ''
  form.manufacturer = ''
  form.description = ''
  form.default_daily_rate = null
  formError.value = null
  showCreate.value = true
}

async function submit(): Promise<void> {
  saving.value = true
  formError.value = null
  try {
    const created = await createLiftType({ ...form })
    items.value.push(created)
    items.value.sort((a, b) => a.name.localeCompare(b.name))
    showCreate.value = false
  } catch (e) {
    formError.value = extractApiError(e, 'Failed to create lift type.')
  } finally {
    saving.value = false
  }
}

async function remove(t: LiftType): Promise<void> {
  if (!window.confirm(`Delete lift type “${t.name}”?`)) return
  error.value = null
  try {
    await deleteLiftType(t.id)
    items.value = items.value.filter((x) => x.id !== t.id)
  } catch (e) {
    error.value = extractApiError(e, 'Failed to delete lift type.')
  }
}

onMounted(load)
</script>
