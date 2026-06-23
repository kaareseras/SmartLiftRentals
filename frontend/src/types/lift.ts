import type { LiftType } from './liftType'

export interface Lift {
  id: number
  uid: string
  name: string
  lift_type_id: number
  lift_type_name: string | null
  model: string | null
  lift_type: LiftType | null
  status: 'available' | 'rented' | 'maintenance' | 'offline' | string
  location: string | null
  latitude: number | null
  longitude: number | null
  battery_voltage: number | null
  telemetry_state: string | null
  last_seen: string | null
  created_at: string
  updated_at: string
}

export interface LiftCreate {
  uid: string
  name: string
  lift_type_id: number
  status?: string
  location?: string | null
  latitude?: number | null
  longitude?: number | null
  last_seen?: string | null
}

export interface LiftUpdate {
  uid?: string
  name?: string
  lift_type_id?: number
  status?: string
  location?: string | null
  latitude?: number | null
  longitude?: number | null
  last_seen?: string | null
}
