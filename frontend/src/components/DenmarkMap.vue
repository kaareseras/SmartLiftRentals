<template>
  <div class="dk-map" :class="{ compact }">
    <div ref="mapEl" class="dk-leaflet" />
    <div v-if="failed" class="dk-fallback">
      <p>Unable to load the map.</p>
      <p class="dk-fallback__hint">Check your internet connection and refresh.</p>
    </div>
    <div v-if="showLegend && !failed" class="dk-legend">
      <span class="dk-legend__item"><i style="background: #0078d4" /> Operating</span>
      <span class="dk-legend__item"><i style="background: #107c10" /> Charging</span>
      <span class="dk-legend__item"><i style="background: #8a8886" /> Idle</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

import { loadLeaflet } from '../utils/leaflet'

export interface MapMarker {
  id: number
  name: string
  lat: number | null
  lng: number | null
  state: string | null
}

const props = withDefaults(
  defineProps<{
    markers: MapMarker[]
    selectedId?: number | null
    showLegend?: boolean
    showLabels?: boolean
    compact?: boolean
  }>(),
  { selectedId: null, showLegend: true, showLabels: false, compact: false },
)

const emit = defineEmits<{ (e: 'select', id: number): void }>()

const mapEl = ref<HTMLElement | null>(null)
const failed = ref(false)

/* eslint-disable @typescript-eslint/no-explicit-any */
let L: any = null
let map: any = null
const layers = new Map<number, any>()
/* eslint-enable @typescript-eslint/no-explicit-any */
let fitted = false

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

function render(): void {
  if (!map || !L) return
  const present = new Set<number>()

  for (const m of props.markers) {
    if (m.lat == null || m.lng == null) continue
    present.add(m.id)
    const style = {
      radius: props.selectedId === m.id ? 11 : 8,
      color: '#ffffff',
      weight: 2,
      fillColor: stateColor(m.state),
      fillOpacity: 1,
    }
    let marker = layers.get(m.id)
    if (!marker) {
      marker = L.circleMarker([m.lat, m.lng], style)
      marker.bindTooltip(m.name, {
        permanent: !!props.showLabels,
        direction: 'top',
        offset: [0, -6],
      })
      marker.on('click', () => emit('select', m.id))
      marker.addTo(map)
      layers.set(m.id, marker)
    } else {
      marker.setStyle(style)
      marker.setLatLng([m.lat, m.lng])
    }
  }

  for (const [id, marker] of layers) {
    if (!present.has(id)) {
      map.removeLayer(marker)
      layers.delete(id)
    }
  }

  if (!fitted) {
    const pts = props.markers.filter((m) => m.lat != null && m.lng != null)
    if (props.compact && pts.length) {
      map.setView([pts[0].lat, pts[0].lng], 11)
      fitted = true
    } else if (pts.length) {
      map.fitBounds(L.latLngBounds(pts.map((p) => [p.lat, p.lng])).pad(0.4))
      fitted = true
    }
  }
}

onMounted(async () => {
  try {
    L = await loadLeaflet()
    if (!mapEl.value) return
    map = L.map(mapEl.value, {
      scrollWheelZoom: !props.compact,
      zoomControl: !props.compact,
    }).setView([56.0, 10.6], props.compact ? 9 : 6)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(map)
    render()
    setTimeout(() => {
      if (map) map.invalidateSize()
    }, 120)
  } catch {
    failed.value = true
  }
})

watch(() => props.markers, render, { deep: true })
watch(() => props.selectedId, render)

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
  layers.clear()
})
</script>

<style scoped>
.dk-map {
  position: relative;
}

.dk-leaflet {
  width: 100%;
  height: 480px;
  border-radius: var(--radius-md);
  overflow: hidden;
  z-index: 0;
}

.dk-map.compact .dk-leaflet {
  height: 320px;
}

.dk-fallback {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  background: var(--color-bg-alt);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
}

.dk-fallback__hint {
  font-size: 0.82rem;
  color: var(--color-text-tertiary);
}

.dk-legend {
  position: absolute;
  bottom: 0.75rem;
  left: 0.75rem;
  z-index: 500;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 0.5rem 0.7rem;
  font-size: 0.78rem;
}

.dk-legend__item {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.dk-legend__item i {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}
</style>
