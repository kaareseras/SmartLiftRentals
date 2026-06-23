export interface Contract {
  id: number
  lift_id: number
  customer_id: number
  start_date: string
  duration_days: number
  daily_rate: number
  status: string
  notes: string | null
  end_date: string | null
  total_price: number
  customer_name: string | null
  lift_name: string | null
  lift_uid: string | null
  created_at: string
  updated_at: string
}

export interface ContractCreate {
  lift_id: number
  customer_id: number
  start_date: string
  duration_days: number
  daily_rate: number
  status?: string
  notes?: string | null
}

export type ContractUpdate = Partial<ContractCreate>
