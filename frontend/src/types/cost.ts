export interface Cost {
  id: number
  lift_id: number
  category: string
  description: string | null
  amount: number
  incurred_on: string
  lift_name: string | null
  lift_uid: string | null
  created_at: string
  updated_at: string
}

export interface CostCreate {
  lift_id: number
  category: string
  description?: string | null
  amount: number
  incurred_on: string
}

export type CostUpdate = Partial<CostCreate>
