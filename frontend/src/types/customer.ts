export interface Customer {
  id: number
  name: string
  email: string | null
  phone: string | null
  company: string | null
  address: string | null
  contract_count: number
  created_at: string
  updated_at: string
}

export interface CustomerCreate {
  name: string
  email?: string | null
  phone?: string | null
  company?: string | null
  address?: string | null
}

export type CustomerUpdate = Partial<CustomerCreate>
