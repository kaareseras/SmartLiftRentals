// Loads Leaflet from a CDN on demand so the map works without bundling the
// dependency (OpenStreetMap tiles already require browser internet access).
// Returns the global `L` namespace once ready.

const LEAFLET_VERSION = '1.9.4'
const CSS_URL = `https://unpkg.com/leaflet@${LEAFLET_VERSION}/dist/leaflet.css`
const JS_URL = `https://unpkg.com/leaflet@${LEAFLET_VERSION}/dist/leaflet.js`

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Leaflet = any

let cached: Promise<Leaflet> | null = null

export function loadLeaflet(): Promise<Leaflet> {
  const existing = (window as unknown as { L?: Leaflet }).L
  if (existing) return Promise.resolve(existing)
  if (cached) return cached

  cached = new Promise<Leaflet>((resolve, reject) => {
    if (!document.getElementById('leaflet-css')) {
      const link = document.createElement('link')
      link.id = 'leaflet-css'
      link.rel = 'stylesheet'
      link.href = CSS_URL
      document.head.appendChild(link)
    }

    const script = document.createElement('script')
    script.src = JS_URL
    script.async = true
    script.onload = () => {
      const L = (window as unknown as { L?: Leaflet }).L
      if (L) resolve(L)
      else reject(new Error('Leaflet failed to initialise'))
    }
    script.onerror = () => reject(new Error('Failed to load Leaflet'))
    document.head.appendChild(script)
  })

  return cached
}
