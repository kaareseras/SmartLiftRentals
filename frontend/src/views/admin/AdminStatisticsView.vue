<template>
  <div class="page">
    <RouterLink to="/admin" class="back-link">← Admin console</RouterLink>

    <header class="admin-page-header">
      <div>
        <h1 class="page-title">Statistics</h1>
        <p class="page-subtitle">Revenue, cost, and profit across the fleet</p>
      </div>
      <button class="btn btn-secondary" :disabled="loading" @click="load">
        {{ loading ? 'Refreshing…' : 'Refresh' }}
      </button>
    </header>

    <div v-if="error" class="alert alert-error" style="margin-bottom: 1.25rem">{{ error }}</div>

    <!-- KPIs -->
    <section class="kpi-grid" style="margin-bottom: 2rem">
      <div class="card card-pad kpi">
        <span class="kpi__label">Total revenue</span>
        <span class="kpi__value">{{ formatCurrency(overview?.total_revenue ?? 0) }}</span>
        <span class="kpi__hint">All contracts</span>
      </div>
      <div class="card card-pad kpi">
        <span class="kpi__label">Total cost</span>
        <span class="kpi__value">{{ formatCurrency(overview?.total_cost ?? 0) }}</span>
        <span class="kpi__hint">All lift costs</span>
      </div>
      <div class="card card-pad kpi">
        <span class="kpi__label">Net profit</span>
        <span
          class="kpi__value"
          :style="{ color: (overview?.net_profit ?? 0) >= 0 ? 'var(--color-success)' : 'var(--color-danger)' }"
        >
          {{ formatCurrency(overview?.net_profit ?? 0) }}
        </span>
        <span class="kpi__hint">Revenue − cost</span>
      </div>
      <div class="card card-pad kpi">
        <span class="kpi__label">Active contracts</span>
        <span class="kpi__value">{{ overview?.active_contracts ?? 0 }}</span>
        <span class="kpi__hint">of {{ overview?.total_contracts ?? 0 }} total</span>
      </div>
    </section>

    <!-- Monthly chart -->
    <section class="card card-pad" style="margin-bottom: 1.5rem">
      <div class="section-head">
        <div>
          <h2 class="section-title">Monthly performance</h2>
          <p class="section-sub">Revenue recognised at contract start date.</p>
        </div>
        <select v-model.number="year" class="select toolbar__select" @change="loadMonthly">
          <option v-for="y in yearOptions" :key="y" :value="y">{{ y }}</option>
        </select>
      </div>

      <div class="legend">
        <span class="legend__item"><span class="legend__swatch swatch-rev" /> Revenue</span>
        <span class="legend__item"><span class="legend__swatch swatch-cost" /> Cost</span>
      </div>

      <div class="chart">
        <div v-for="m in monthly" :key="m.month" class="chart__col">
          <div class="chart__bars">
            <div
              class="chart__bar swatch-rev"
              :style="{ height: barHeight(m.revenue) }"
              :title="`Revenue: ${formatCurrency(m.revenue)}`"
            />
            <div
              class="chart__bar swatch-cost"
              :style="{ height: barHeight(m.cost) }"
              :title="`Cost: ${formatCurrency(m.cost)}`"
            />
          </div>
          <span class="chart__label">{{ m.label }}</span>
        </div>
      </div>
    </section>

    <div class="stats-cols">
      <!-- Yearly table -->
      <section class="card table-card">
        <div class="card-pad" style="padding-bottom: 0.5rem">
          <h2 class="section-title">By year</h2>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>Year</th>
              <th class="text-right">Revenue</th>
              <th class="text-right">Cost</th>
              <th class="text-right">Profit</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="y in yearly" :key="y.year">
              <td class="cell-strong">{{ y.year }}</td>
              <td class="cell-num">{{ formatCurrency(y.revenue) }}</td>
              <td class="cell-num">{{ formatCurrency(y.cost) }}</td>
              <td class="cell-num" :class="y.profit >= 0 ? 'pos' : 'neg'">{{ formatCurrency(y.profit) }}</td>
            </tr>
            <tr v-if="yearly.length === 0"><td colspan="4" class="cell-muted" style="text-align:center">No data</td></tr>
          </tbody>
        </table>
      </section>

      <!-- By lift table -->
      <section class="card table-card">
        <div class="card-pad" style="padding-bottom: 0.5rem">
          <h2 class="section-title">By lift</h2>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>Lift</th>
              <th class="text-right">Revenue</th>
              <th class="text-right">Cost</th>
              <th class="text-right">Profit</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="l in byLift" :key="l.lift_id">
              <td>
                <div class="cell-strong">{{ l.name }}</div>
                <div class="cell-muted" style="font-size: 0.78rem">{{ l.lift_type_name }}</div>
              </td>
              <td class="cell-num">{{ formatCurrency(l.revenue) }}</td>
              <td class="cell-num">{{ formatCurrency(l.cost) }}</td>
              <td class="cell-num" :class="l.profit >= 0 ? 'pos' : 'neg'">{{ formatCurrency(l.profit) }}</td>
            </tr>
            <tr v-if="byLift.length === 0"><td colspan="4" class="cell-muted" style="text-align:center">No data</td></tr>
          </tbody>
        </table>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import {
  fetchByLift,
  fetchMonthly,
  fetchOverview,
  fetchYearly,
} from '../../api/statistics'
import type { LiftStat, MonthlyStat, OverviewStats, YearlyStat } from '../../types/statistics'
import { extractApiError, formatCurrency } from '../../utils/format'

const overview = ref<OverviewStats | null>(null)
const monthly = ref<MonthlyStat[]>([])
const yearly = ref<YearlyStat[]>([])
const byLift = ref<LiftStat[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const year = ref(new Date().getFullYear())

const yearOptions = computed(() => {
  const years = new Set<number>(yearly.value.map((y) => y.year))
  years.add(new Date().getFullYear())
  years.add(year.value)
  return [...years].sort((a, b) => b - a)
})

const chartMax = computed(() => {
  const values = monthly.value.flatMap((m) => [m.revenue, m.cost])
  return Math.max(1, ...values)
})

function barHeight(value: number): string {
  const pct = (value / chartMax.value) * 100
  return `${Math.max(value > 0 ? 2 : 0, pct)}%`
}

async function loadMonthly(): Promise<void> {
  try {
    monthly.value = await fetchMonthly(year.value)
  } catch (e) {
    error.value = extractApiError(e, 'Failed to load monthly statistics.')
  }
}

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    const [ov, mon, yr, bl] = await Promise.all([
      fetchOverview(),
      fetchMonthly(year.value),
      fetchYearly(),
      fetchByLift(),
    ])
    overview.value = ov
    monthly.value = mon
    yearly.value = yr
    byLift.value = bl
  } catch (e) {
    error.value = extractApiError(e, 'Failed to load statistics.')
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.section-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.section-title {
  font-size: 1.1rem;
}

.section-sub {
  margin-top: 0.2rem;
  font-size: 0.82rem;
  color: var(--color-text-tertiary);
}

.legend {
  display: flex;
  gap: 1.25rem;
  margin-bottom: 1rem;
  font-size: 0.8rem;
  color: var(--color-text-secondary);
}

.legend__item {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.legend__swatch {
  width: 12px;
  height: 12px;
  border-radius: 3px;
  display: inline-block;
}

.swatch-rev {
  background: var(--color-primary);
}

.swatch-cost {
  background: #d9822b;
}

.chart {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 0.5rem;
  height: 200px;
  align-items: end;
}

.chart__col {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  justify-content: flex-end;
  gap: 0.4rem;
}

.chart__bars {
  display: flex;
  align-items: flex-end;
  gap: 3px;
  height: 100%;
  width: 100%;
  justify-content: center;
}

.chart__bar {
  width: 38%;
  min-width: 6px;
  border-radius: 3px 3px 0 0;
  transition: height 0.3s ease;
}

.chart__label {
  font-size: 0.7rem;
  color: var(--color-text-tertiary);
}

.stats-cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  align-items: start;
}

@media (max-width: 860px) {
  .stats-cols {
    grid-template-columns: 1fr;
  }
}
</style>
