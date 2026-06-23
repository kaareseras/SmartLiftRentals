<template>
  <div class="page admin">
    <header class="page-header admin__header">
      <div>
        <div class="page-eyebrow">Administration</div>
        <h1 class="page-title">Platform admin console</h1>
        <p class="page-subtitle">
          Welcome back, {{ auth.user?.name }}. Manage users, fleet inventory, and platform
          configuration.
        </p>
      </div>
      <button class="btn btn-secondary" :disabled="loading" @click="load">
        <span v-if="loading" class="spinner admin__refresh-spinner" />
        {{ loading ? 'Refreshing…' : 'Refresh' }}
      </button>
    </header>

    <div v-if="error" class="alert alert-error admin__alert">{{ error }}</div>

    <!-- KPIs -->
    <section class="kpi-grid" style="margin-bottom: 2.5rem">
      <div class="card card-pad kpi">
        <span class="kpi__label">Net profit</span>
        <span
          class="kpi__value"
          :style="{ color: (overview?.net_profit ?? 0) >= 0 ? 'var(--color-success)' : 'var(--color-danger)' }"
        >{{ formatCurrency(overview?.net_profit ?? 0) }}</span>
        <span class="kpi__hint">Revenue − cost</span>
      </div>
      <div class="card card-pad kpi">
        <span class="kpi__label">Total revenue</span>
        <span class="kpi__value">{{ formatCurrency(overview?.total_revenue ?? 0) }}</span>
        <span class="kpi__hint">{{ overview?.total_contracts ?? 0 }} contracts</span>
      </div>
      <div class="card card-pad kpi">
        <span class="kpi__label">Active rentals</span>
        <span class="kpi__value">{{ overview?.active_contracts ?? 0 }}</span>
        <span class="kpi__hint">Currently out</span>
      </div>
      <div class="card card-pad kpi">
        <span class="kpi__label">Fleet size</span>
        <span class="kpi__value">{{ overview?.total_lifts ?? 0 }}</span>
        <span class="kpi__hint">{{ overview?.total_lift_types ?? 0 }} types</span>
      </div>
    </section>

    <!-- Management areas -->
    <h2 class="admin__section-title">Management areas</h2>
    <section class="admin__grid">
      <RouterLink
        v-for="area in areas"
        :key="area.to"
        :to="area.to"
        class="card card-pad admin-card"
      >
        <span class="admin-card__icon" v-html="area.icon" />
        <h3 class="admin-card__title">{{ area.title }}</h3>
        <p class="admin-card__text">{{ area.text }}</p>
        <span class="admin-card__cta">{{ area.cta }} →</span>
      </RouterLink>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import { fetchOverview } from '../../api/statistics'
import { useAuthStore } from '../../stores/auth'
import type { OverviewStats } from '../../types/statistics'
import { extractApiError, formatCurrency } from '../../utils/format'

const auth = useAuthStore()

const overview = ref<OverviewStats | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const icons = {
  users:
    '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
  types:
    '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 2 7l10 5 10-5-10-5Z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/></svg>',
  fleet:
    '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
  customers:
    '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
  contracts:
    '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M9 13h6"/><path d="M9 17h4"/></svg>',
  costs:
    '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
  statistics:
    '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
  telemetry:
    '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
}

const areas = [
  { to: '/admin/telemetry', title: 'Live telemetry', text: 'Track lift positions on a map of Denmark with live battery and status.', cta: 'Open live map', icon: icons.telemetry },
  { to: '/admin/statistics', title: 'Statistics', text: 'Revenue, cost, and profit trends per month, year, and lift.', cta: 'View analytics', icon: icons.statistics },
  { to: '/admin/contracts', title: 'Contracts', text: 'Rent lifts to customers and manage durations and pricing.', cta: 'Manage rentals', icon: icons.contracts },
  { to: '/admin/customers', title: 'Customers', text: 'Maintain the customer directory and contact details.', cta: 'Manage customers', icon: icons.customers },
  { to: '/admin/costs', title: 'Costs', text: 'Track maintenance, repair, and operating costs per lift.', cta: 'Manage costs', icon: icons.costs },
  { to: '/lifts', title: 'Fleet', text: 'Register and monitor every rental lift in the fleet.', cta: 'Open fleet', icon: icons.fleet },
  { to: '/admin/lift-types', title: 'Lift types', text: 'Manage the catalogue of lift models and default rates.', cta: 'Manage types', icon: icons.types },
  { to: '/admin/users', title: 'Users', text: 'Create accounts and control platform access and roles.', cta: 'Manage users', icon: icons.users },
]

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    overview.value = await fetchOverview()
  } catch (e) {
    error.value = extractApiError(e, 'Failed to load admin data.')
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.admin__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.admin__alert {
  margin-bottom: 1.25rem;
}

.admin__refresh-spinner {
  width: 14px;
  height: 14px;
  border-width: 2px;
}

/* KPIs */
.kpis {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.kpi {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.kpi__label {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.kpi__value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-heading);
  line-height: 1.1;
}

.kpi__hint {
  font-size: 0.78rem;
  color: var(--color-text-tertiary);
}

/* Areas */
.admin__section-title {
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.admin__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}

.admin-card {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: var(--color-text);
  transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
}

a.admin-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary);
  text-decoration: none;
}

.admin-card--soon {
  opacity: 0.75;
}

.admin-card__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background: var(--color-primary-soft);
  color: var(--color-primary-pressed);
  margin-bottom: 1rem;
}

.admin-card__title {
  font-size: 1.05rem;
  margin-bottom: 0.35rem;
}

.admin-card__text {
  color: var(--color-text-secondary);
  font-size: 0.88rem;
  line-height: 1.5;
  flex: 1;
}

.admin-card__cta {
  margin-top: 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-primary);
}

@media (max-width: 960px) {
  .kpis {
    grid-template-columns: repeat(2, 1fr);
  }

  .admin__grid {
    grid-template-columns: 1fr;
  }
}
</style>
