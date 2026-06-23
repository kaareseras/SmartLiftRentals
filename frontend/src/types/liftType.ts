export interface LiftType {
  id: number
  name: string
  model: string
  manufacturer: string | null
  description: string | null
  default_daily_rate: number | null
  lift_count: number
  created_at: string
  updated_at: string
}

export interface LiftTypeCreate {
  name: string
  model: string
  manufacturer?: string | null
  description?: string | null
  default_daily_rate?: number | null
}

export type LiftTypeUpdate = Partial<LiftTypeCreate>
