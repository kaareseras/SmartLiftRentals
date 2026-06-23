export function formatCurrency(value: number | null | undefined): string {
  return new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency: 'DKK',
    maximumFractionDigits: 0,
  }).format(value ?? 0)
}

export function formatDate(value: string | null | undefined): string {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}

export function initialsOf(name: string | null | undefined): string {
  if (!name) return 'U'
  return (
    name
      .trim()
      .split(/\s+/)
      .map((part) => part[0])
      .slice(0, 2)
      .join('')
      .toUpperCase() || 'U'
  )
}

export function liftStatusBadge(status: string): string {
  switch (status) {
    case 'available':
      return 'badge-green'
    case 'rented':
      return 'badge-blue'
    case 'maintenance':
      return 'badge-amber'
    case 'offline':
      return 'badge-red'
    default:
      return 'badge-gray'
  }
}

export function contractStatusBadge(status: string): string {
  switch (status) {
    case 'active':
      return 'badge-green'
    case 'completed':
      return 'badge-blue'
    case 'cancelled':
      return 'badge-red'
    default:
      return 'badge-gray'
  }
}

export function costCategoryBadge(category: string): string {
  switch (category) {
    case 'maintenance':
      return 'badge-blue'
    case 'repair':
      return 'badge-amber'
    case 'insurance':
      return 'badge-gray'
    case 'transport':
      return 'badge-green'
    default:
      return 'badge-gray'
  }
}

export function telemetryStateBadge(state: string | null): string {
  switch (state) {
    case 'operating':
      return 'badge-blue'
    case 'charging':
      return 'badge-green'
    case 'idle':
      return 'badge-gray'
    default:
      return 'badge-gray'
  }
}

export function telemetryStateLabel(state: string | null): string {
  if (!state) return 'Unknown'
  return state.charAt(0).toUpperCase() + state.slice(1)
}

export function batteryColor(voltage: number | null): string {
  if (voltage == null) return 'var(--color-text-tertiary)'
  if (voltage >= 24.5) return 'var(--color-success)'
  if (voltage >= 23) return 'var(--color-warning)'
  return 'var(--color-danger)'
}

export function batteryPercent(voltage: number | null): number {
  if (voltage == null) return 0
  const pct = ((voltage - 21.5) / (26.5 - 21.5)) * 100
  return Math.max(0, Math.min(100, Math.round(pct)))
}

export function relativeTime(value: string | null): string {
  if (!value) return '—'
  const then = new Date(value).getTime()
  if (Number.isNaN(then)) return '—'
  const seconds = Math.max(0, Math.round((Date.now() - then) / 1000))
  if (seconds < 10) return 'just now'
  if (seconds < 60) return `${seconds}s ago`
  const minutes = Math.round(seconds / 60)
  if (minutes < 60) return `${minutes}m ago`
  const hours = Math.round(minutes / 60)
  if (hours < 24) return `${hours}h ago`
  return `${Math.round(hours / 24)}d ago`
}

export function extractApiError(error: unknown, fallback: string): string {
  const e = error as { response?: { data?: { detail?: unknown } } }
  const detail = e?.response?.data?.detail
  if (typeof detail === 'string') return detail
  return fallback
}
