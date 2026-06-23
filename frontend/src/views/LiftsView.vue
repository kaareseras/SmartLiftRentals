<template>
  <div class="page lifts">
    <header class="page-header">
      <div class="page-eyebrow">Fleet</div>
      <h1 class="page-title">Lift inventory</h1>
      <p class="page-subtitle">Register and monitor every rental lift in your fleet.</p>
    </header>

    <div v-if="error" class="alert alert-error" style="margin-bottom: 1.25rem">{{ error }}</div>

    <!-- Add lift -->
    <div class="card card-pad lifts__form-card">
      <h2 class="lifts__form-title">Register a lift</h2>
      <p v-if="liftTypes.length === 0 && !loadingTypes" class="field-hint" style="margin-bottom: 1rem">
        No lift types yet — an administrator must add a lift type first.
      </p>
      <form class="lifts__form" @submit.prevent="submit">
        <div class="field">
          <label class="label" for="uid">UID</label>
          <input id="uid" v-model="form.uid" class="input" placeholder="LFT-0001" required />
        </div>
        <div class="field">
          <label class="label" for="name">Name</label>
          <input id="name" v-model="form.name" class="input" placeholder="Tower Crane North" required />
        </div>
        <div class="field">
          <label class="label" for="type">Lift type</label>
          <select id="type" v-model.number="form.lift_type_id" class="select" required>
            <option :value="0" disabled>Select a type…</option>
            <option v-for="t in liftTypes" :key="t.id" :value="t.id">{{ t.name }} — {{ t.model }}</option>
          </select>
        </div>
        <div class="field">
          <label class="label" for="status">Status</label>
          <select id="status" v-model="form.status" class="select">
            <option value="available">Available</option>
            <option value="rented">Rented</option>
            <option value="maintenance">Maintenance</option>
            <option value="offline">Offline</option>
          </select>
        </div>
        <button class="btn btn-primary lifts__submit" type="submit" :disabled="saving || liftTypes.length === 0">
          {{ saving ? 'Adding…' : 'Add lift' }}
        </button>
      </form>
    </div>

    <!-- Fleet table -->
    <div v-if="store.loading" class="state card">
      <span class="spinner" />
      <p>Loading lifts…</p>
    </div>

    <div v-else-if="store.lifts.length === 0" class="state card">
      <p>No lifts registered yet. Add your first lift above.</p>
    </div>

    <div v-else class="card table-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>UID</th>
            <th>Type</th>
            <th>Status</th>
            <th class="text-right">Battery</th>
            <th>State</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lift in store.lifts" :key="lift.id">
            <td class="cell-strong">
              <RouterLink v-if="auth.isAdmin" class="lift-link" :to="`/admin/lifts/${lift.id}`">{{ lift.name }}</RouterLink>
              <span v-else>{{ lift.name }}</span>
            </td>
            <td class="mono">{{ lift.uid }}</td>
            <td>{{ lift.lift_type_name || '—' }}</td>
            <td>
              <span class="badge" :class="liftStatusBadge(lift.status)">{{ lift.status }}</span>
            </td>
            <td class="cell-num" :style="{ color: batteryColor(lift.battery_voltage) }">
              {{ lift.battery_voltage != null ? lift.battery_voltage.toFixed(1) + ' V' : '—' }}
            </td>
            <td>
              <span class="badge" :class="telemetryStateBadge(lift.telemetry_state)">{{ telemetryStateLabel(lift.telemetry_state) }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { RouterLink } from 'vue-router'

import { fetchLiftTypes } from '../api/liftTypes'
import { useLiftStore } from '../stores/lifts'
import { useAuthStore } from '../stores/auth'
import type { LiftCreate } from '../types/lift'
import type { LiftType } from '../types/liftType'
import {
  batteryColor,
  extractApiError,
  liftStatusBadge,
  telemetryStateBadge,
  telemetryStateLabel,
} from '../utils/format'

const store = useLiftStore()
const auth = useAuthStore()
const liftTypes = ref<LiftType[]>([])
const loadingTypes = ref(false)
const saving = ref(false)
const error = ref<string | null>(null)

const form = reactive<LiftCreate>({
  uid: '',
  name: '',
  lift_type_id: 0,
  status: 'available',
  location: null,
  latitude: null,
  longitude: null,
  last_seen: null,
})

async function submit(): Promise<void> {
  saving.value = true
  error.value = null
  try {
    await store.addLift({ ...form })
    form.uid = ''
    form.name = ''
    form.lift_type_id = 0
    form.status = 'available'
  } catch (e) {
    error.value = extractApiError(e, 'Failed to add lift.')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  loadingTypes.value = true
  try {
    const [types] = await Promise.all([fetchLiftTypes(), store.loadLifts()])
    liftTypes.value = types
  } catch (e) {
    error.value = extractApiError(e, 'Failed to load lift types.')
  } finally {
    loadingTypes.value = false
  }
})
</script>

<style scoped>
.lifts__form-card {
  margin-bottom: 1.5rem;
}

.lifts__form-title {
  font-size: 1.05rem;
  margin-bottom: 1rem;
}

.lifts__form {
  display: grid;
  grid-template-columns: repeat(4, 1fr) auto;
  gap: 1rem;
  align-items: end;
}

.lifts__form .field {
  margin-bottom: 0;
}

.lifts__submit {
  height: 36px;
}

.state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

@media (max-width: 760px) {
  .lifts__form {
    grid-template-columns: 1fr;
  }
}
</style>
