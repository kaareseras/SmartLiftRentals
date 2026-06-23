export interface LiftTelemetry {
  id: number
  uid: string
  name: string
  status: string
  lift_type_name: string | null
  location: string | null
  latitude: number | null
  longitude: number | null
  battery_voltage: number | null
  telemetry_state: string | null
  last_seen: string | null
}
