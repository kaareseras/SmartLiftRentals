<template>
  <div class="page">
    <RouterLink to="/admin/telemetry" class="back-link">← Live telemetry</RouterLink>

    <div v-if="error" class="alert alert-error" style="margin-bottom: 1.25rem">{{ error }}</div>

    <div v-if="loading && !lift" class="state card"><span class="spinner" /><p>Loading…</p></div>

    <template v-else-if="lift">
      <header class="admin-page-header">
        <div>
          <div class="page-eyebrow">{{ lift.lift_type_name || 'Lift' }}</div>
          <h1 class="page-title">{{ lift.name }}</h1>
          <p class="page-subtitle">
            <span class="mono">{{ lift.uid }}</span> · {{ lift.model || '—' }} · {{ lift.location || '—' }}
          </p>
        </div>
        <span class="badge" :class="liftStatusBadge(lift.status)">{{ lift.status }}</span>
      </header>

      <!-- Live status -->
      <section class="kpi-grid" style="margin-bottom: 1.5rem">
        <div class="card card-pad kpi">
          <span class="kpi__label">Battery</span>
          <span class="kpi__value" :style="{ color: batteryColor(lift.battery_voltage) }">
            {{ lift.battery_voltage != null ? lift.battery_voltage.toFixed(1) + ' V' : '—' }}
          </span>
          <div class="batt-bar" style="margin-top: 0.4rem">
            <div class="batt-fill" :style="{ width: batteryPercent(lift.battery_voltage) + '%', background: batteryColor(lift.battery_voltage) }" />
          </div>
        </div>
        <div class="card card-pad kpi">
          <span class="kpi__label">Telemetry state</span>
          <span class="kpi__value" style="font-size: 1.3rem; margin-top: 0.3rem">
            <span class="badge" :class="telemetryStateBadge(lift.telemetry_state)">{{ telemetryStateLabel(lift.telemetry_state) }}</span>
          </span>
          <span class="kpi__hint">{{ liveLabel }}</span>
        </div>
        <div class="card card-pad kpi">
          <span class="kpi__label">Operational status</span>
          <span class="kpi__value" style="font-size: 1.3rem; margin-top: 0.3rem">
            <span class="badge" :class="liftStatusBadge(lift.status)">{{ lift.status }}</span>
          </span>
        </div>
        <div class="card card-pad kpi">
          <span class="kpi__label">Last seen</span>
          <span class="kpi__value" style="font-size: 1.3rem">{{ relativeTime(lift.last_seen) }}</span>
          <span class="kpi__hint">{{ formatDate(lift.last_seen) }}</span>
        </div>
      </section>

      <!-- Map + position details -->
      <div class="detail-cols">
        <div class="card map-card-sm">
          <DenmarkMap :markers="markers" :show-legend="false" show-labels />
        </div>
        <div class="card card-pad">
          <h2 class="detail-h2">Position &amp; device</h2>
          <dl class="detail-dl">
            <div><dt>Location</dt><dd>{{ lift.location || '—' }}</dd></div>
            <div><dt>Latitude</dt><dd class="mono">{{ lift.latitude?.toFixed(4) ?? '—' }}</dd></div>
            <div><dt>Longitude</dt><dd class="mono">{{ lift.longitude?.toFixed(4) ?? '—' }}</dd></div>
            <div><dt>Lift type</dt><dd>{{ lift.lift_type_name || '—' }}</dd></div>
            <div><dt>Model</dt><dd>{{ lift.model || '—' }}</dd></div>
            <div><dt>Battery</dt><dd :style="{ color: batteryColor(lift.battery_voltage) }">{{ lift.battery_voltage != null ? lift.battery_voltage.toFixed(2) + ' V' : '—' }}</dd></div>
          </dl>
        </div>
      </div>

      <!-- Financials -->
      <section class="kpi-grid" style="margin: 1.5rem 0">
        <div class="card card-pad kpi">
          <span class="kpi__label">Revenue</span>
          <span class="kpi__value">{{ formatCurrency(stats?.revenue ?? 0) }}</span>
        </div>
        <div class="card card-pad kpi">
          <span class="kpi__label">Cost</span>
          <span class="kpi__value">{{ formatCurrency(stats?.cost ?? 0) }}</span>
        </div>
        <div class="card card-pad kpi">
          <span class="kpi__label">Profit</span>
          <span class="kpi__value" :style="{ color: (stats?.profit ?? 0) >= 0 ? 'var(--color-success)' : 'var(--color-danger)' }">
            {{ formatCurrency(stats?.profit ?? 0) }}
          </span>
        </div>
        <div class="card card-pad kpi">
          <span class="kpi__label">Contracts</span>
          <span class="kpi__value">{{ contracts.length }}</span>
        </div>
      </section>

      <!-- Contracts -->
      <h2 class="detail-section-title">Contracts</h2>
      <div v-if="contracts.length === 0" class="state card" style="margin-bottom: 1.5rem"><p>No contracts for this lift.</p></div>
      <div v-else class="card table-card" style="margin-bottom: 1.5rem">
        <table class="data-table">
          <thead>
            <tr>
              <th>Customer</th><th>Start</th><th>End</th>
              <th class="text-right">Days</th><th class="text-right">Day rate</th>
              <th class="text-right">Total</th><th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in contracts" :key="c.id">
              <td class="cell-strong">{{ c.customer_name }}</td>
              <td class="cell-muted">{{ formatDate(c.start_date) }}</td>
              <td class="cell-muted">{{ formatDate(c.end_date) }}</td>
              <td class="cell-num">{{ c.duration_days }}</td>
              <td class="cell-num">{{ formatCurrency(c.daily_rate) }}</td>
              <td class="cell-num cell-strong">{{ formatCurrency(c.total_price) }}</td>
              <td><span class="badge" :class="contractStatusBadge(c.status)">{{ c.status }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Costs -->
      <h2 class="detail-section-title">Costs</h2>
      <div v-if="costs.length === 0" class="state card"><p>No costs for this lift.</p></div>
      <div v-else class="card table-card">
        <table class="data-table">
          <thead>
            <tr><th>Date</th><th>Category</th><th>Description</th><th class="text-right">Amount</th></tr>
          </thead>
          <tbody>
            <tr v-for="c in costs" :key="c.id">
              <td class="cell-muted">{{ formatDate(c.incurred_on) }}</td>
              <td><span class="badge" :class="costCategoryBadge(c.category)">{{ labelize(c.category) }}</span></td>
              <td class="cell-muted">{{ c.description || '—' }}</td>
              <td class="cell-num cell-strong">{{ formatCurrency(c.amount) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

import DenmarkMap from '../../components/DenmarkMap.vue'
import { fetchLift } from '../../api/lifts'
import { fetchContracts } from '../../api/contracts'
import { fetchCosts } from '../../api/costs'
import { fetchLiftStatDetail } from '../../api/statistics'
import type { Lift } from '../../types/lift'
import type { Contract } from '../../types/contract'
import type { Cost } from '../../types/cost'
import type { LiftStatDetail } from '../../types/statistics'
import {
  batteryColor,
  batteryPercent,
  contractStatusBadge,
  costCategoryBadge,
  extractApiError,
  formatCurrency,
  formatDate,
  liftStatusBadge,
  relativeTime,
  telemetryStateBadge,
  telemetryStateLabel,
} from '../../utils/format'

const route = useRoute()
const liftId = computed(() => Number(route.params.id))

const lift = ref<Lift | null>(null)
const contracts = ref<Contract[]>([])
const costs = ref<Cost[]>([])
const stats = ref<LiftStatDetail | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
let timer: ReturnType<typeof setInterval> | undefined

const markers = computed(() =>
  lift.value
    ? [
        {
          id: lift.value.id,
          name: lift.value.name,
          lat: lift.value.latitude,
          lng: lift.value.longitude,
          state: lift.value.telemetry_state,
        },
      ]
    : [],
)

const liveLabel = computed(() =>
  lift.value?.last_seen ? `Updated ${relativeTime(lift.value.last_seen)}` : 'No signal',
)

function labelize(value: string): string {
  return value.charAt(0).toUpperCase() + value.slice(1)
}

async function loadAll(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    const id = liftId.value
    const [liftData, contractData, costData, statData] = await Promise.all([
      fetchLift(id),
      fetchContracts(id),
      fetchCosts(id),
      fetchLiftStatDetail(id, new Date().getFullYear()),
    ])
    lift.value = liftData
    contracts.value = contractData
    costs.value = costData
    stats.value = statData
  } catch (e) {
    error.value = extractApiError(e, 'Failed to load lift details.')
  } finally {
    loading.value = false
  }
}

async function refreshLive(): Promise<void> {
  try {
    lift.value = await fetchLift(liftId.value)
  } catch {
    // keep last known values on a transient error
  }
}

onMounted(() => {
  void loadAll()
  timer = setInterval(() => {
    if (document.visibilityState === 'visible') void refreshLive()
  }, 5000)
})

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.detail-cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  align-items: start;
}

.map-card-sm {
  padding: 0.75rem;
}

.detail-h2,
.detail-section-title {
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.detail-section-title {
  margin-top: 0.5rem;
}

.detail-dl {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.9rem 1.5rem;
  margin: 0;
}

.detail-dl dt {
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--color-text-tertiary);
  margin-bottom: 0.15rem;
}

.detail-dl dd {
  margin: 0;
  font-weight: 600;
  color: var(--color-heading);
}

.batt-bar {
  width: 100%;
  height: 7px;
  border-radius: 4px;
  background: var(--color-bg-alt);
  overflow: hidden;
}

.batt-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.4s ease;
}

.state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 2.5rem 1rem;
  color: var(--color-text-secondary);
}

@media (max-width: 900px) {
  .detail-cols {
    grid-template-columns: 1fr;
  }
}
</style>
