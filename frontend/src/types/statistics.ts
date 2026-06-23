export interface OverviewStats {
  total_lifts: number
  total_lift_types: number
  total_customers: number
  total_contracts: number
  active_contracts: number
  total_revenue: number
  total_cost: number
  net_profit: number
}

export interface MonthlyStat {
  year: number
  month: number
  label: string
  revenue: number
  cost: number
  profit: number
  contracts: number
}

export interface YearlyStat {
  year: number
  revenue: number
  cost: number
  profit: number
  contracts: number
}

export interface LiftStat {
  lift_id: number
  uid: string
  name: string
  lift_type_name: string | null
  revenue: number
  cost: number
  profit: number
  contracts: number
}

export interface LiftStatDetail extends LiftStat {
  monthly: MonthlyStat[]
  yearly: YearlyStat[]
}
