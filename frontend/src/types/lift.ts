export interface Lift {
  id: number
  uid: string
  name: string
  model: string
  status: 'available' | 'rented' | 'maintenance' | 'offline' | string
  location: string | null
  latitude: number | null
  longitude: number | null
  last_seen: string | null
  created_at: string
  updated_at: string
}

export interface LiftCreate {
  uid: string
  name: string
  model: string
  status?: string
  location?: string | null
  latitude?: number | null
  longitude?: number | null
  last_seen?: string | null
}

export interface LiftUpdate {
  uid?: string
  name?: string
  model?: string
  status?: string
  location?: string | null
  latitude?: number | null
  longitude?: number | null
  last_seen?: string | null
}
