<template>
  <div class="page">
    <RouterLink to="/admin" class="back-link">← Admin console</RouterLink>

    <header class="admin-page-header">
      <div>
        <h1 class="page-title">Live telemetry</h1>
        <p class="page-subtitle">
          Real-time position, battery, and operating state across the fleet.
        </p>
      </div>
      <div class="tele-status">
        <span class="live-dot" :class="{ stale: !ticking }" />
        <span>{{ ticking ? 'Live' : 'Paused' }}</span>
        <span class="tele-status__time">updated {{ lastUpdatedLabel }}</span>
      </div>
    </header>

    <div v-if="error" class="alert alert-error" style="margin-bottom: 1.25rem">{{ error }}</div>

    <div class="tele-layout">
      <!-- Map -->
      <div class="card map-card">
        <DenmarkMap :markers="mapMarkers" :selected-id="selectedId" @select="selectedId = $event" />
      </div>

      <!-- List -->
      <div class="card tele-list">
        <div v-if="loading && items.length === 0" class="state"><span class="spinner" /><p>Loading…</p></div>
        <ul v-else class="tele-items">
          <li
            v-for="t in items"
            :key="t.id"
            class="tele-item"
            :class="{ selected: selectedId === t.id }"
            @click="selectedId = t.id"
          >
            <div class="tele-item__head">
              <span class="tele-item__dot" :style="{ background: stateColor(t.telemetry_state) }" />
              <div class="tele-item__title">
                <span class="tele-item__name">{{ t.name }}</span>
                <span class="tele-item__loc">{{ t.location || '—' }} · {{ t.uid }}</span>
              </div>
              <span class="badge" :class="telemetryStateBadge(t.telemetry_state)">
                {{ telemetryStateLabel(t.telemetry_state) }}
              </span>
            </div>
            <div class="tele-item__battery">
              <div class="batt-bar">
                <div
                  class="batt-fill"
                  :style="{ width: batteryPercent(t.battery_voltage) + '%', background: batteryColor(t.battery_voltage) }"
                />
              </div>
              <span class="batt-volt" :style="{ color: batteryColor(t.battery_voltage) }">
                {{ t.battery_voltage != null ? t.battery_voltage.toFixed(1) + ' V' : '—' }}
              </span>
              <RouterLink class="tele-item__link" :to="`/admin/lifts/${t.id}`" @click.stop>Details →</RouterLink>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import DenmarkMap from '../../components/DenmarkMap.vue'
import { fetchTelemetry } from '../../api/telemetry'
import type { LiftTelemetry } from '../../types/telemetry'
import {
  batteryColor,
  batteryPercent,
  extractApiError,
  relativeTime,
  telemetryStateBadge,
  telemetryStateLabel,
} from '../../utils/format'

const items = ref<LiftTelemetry[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const selectedId = ref<number | null>(null)
const lastUpdated = ref<number>(0)
const ticking = ref(true)
let timer: ReturnType<typeof setInterval> | undefined

const markers = computed(() =>
  items.value
    .filter((t) => t.latitude != null && t.longitude != null)
    .map((t) => ({
      id: t.id,
      name: t.name,
      lat: t.latitude,
      lng: t.longitude,
      state: t.telemetry_state,
    })),
)
const mapMarkers = markers

const lastUpdatedLabel = computed(() =>
  lastUpdated.value ? relativeTime(new Date(lastUpdated.value).toISOString()) : '—',
)

function stateColor(state: string | null): string {
  switch (state) {
    case 'operating':
      return '#0078d4'
    case 'charging':
      return '#107c10'
    default:
      return '#8a8886'
  }
}

async function load(): Promise<void> {
  if (items.value.length === 0) loading.value = true
  try {
    items.value = await fetchTelemetry()
    lastUpdated.value = Date.now()
    error.value = null
  } catch (e) {
    error.value = extractApiError(e, 'Failed to load telemetry.')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  void load()
  timer = setInterval(() => {
    if (document.visibilityState === 'visible') {
      ticking.value = true
      void load()
    } else {
      ticking.value = false
    }
  }, 5000)
})

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.tele-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.tele-status__time {
  font-weight: 400;
  color: var(--color-text-tertiary);
}

.live-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--color-success);
  box-shadow: 0 0 0 0 rgba(16, 124, 16, 0.5);
  animation: live 1.8s ease-out infinite;
}

.live-dot.stale {
  background: var(--color-text-tertiary);
  animation: none;
}

@keyframes live {
  0% { box-shadow: 0 0 0 0 rgba(16, 124, 16, 0.5); }
  70% { box-shadow: 0 0 0 7px rgba(16, 124, 16, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 124, 16, 0); }
}

.tele-layout {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 1.5rem;
  align-items: start;
}

.map-card {
  padding: 1rem;
  position: relative;
}

/* list */
.tele-list {
  padding: 0.5rem;
}

.tele-items {
  list-style: none;
  margin: 0;
  padding: 0;
}

.tele-item {
  padding: 0.85rem 0.85rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  border: 1px solid transparent;
}

.tele-item:hover {
  background: var(--color-bg-alt);
}

.tele-item.selected {
  background: var(--color-primary-tint);
  border-color: var(--color-primary);
}

.tele-item__head {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.tele-item__dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.tele-item__title {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.tele-item__name {
  font-weight: 600;
  color: var(--color-heading);
}

.tele-item__loc {
  font-size: 0.78rem;
  color: var(--color-text-tertiary);
}

.tele-item__battery {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-top: 0.5rem;
  padding-left: 1.2rem;
}

.batt-bar {
  flex: 1;
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

.batt-volt {
  font-size: 0.82rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  min-width: 48px;
  text-align: right;
}

.tele-item__link {
  font-size: 0.78rem;
  font-weight: 600;
  white-space: nowrap;
}

.state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 3rem 1rem;
  color: var(--color-text-secondary);
}

@media (max-width: 900px) {
  .tele-layout {
    grid-template-columns: 1fr;
  }
}
</style>
