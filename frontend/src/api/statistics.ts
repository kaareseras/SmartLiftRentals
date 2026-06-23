import apiClient from './index'
import type {
  LiftStat,
  LiftStatDetail,
  MonthlyStat,
  OverviewStats,
  YearlyStat,
} from '../types/statistics'

export async function fetchOverview(): Promise<OverviewStats> {
  const { data } = await apiClient.get<OverviewStats>('/statistics/overview')
  return data
}

export async function fetchMonthly(year: number): Promise<MonthlyStat[]> {
  const { data } = await apiClient.get<MonthlyStat[]>('/statistics/monthly', { params: { year } })
  return data
}

export async function fetchYearly(): Promise<YearlyStat[]> {
  const { data } = await apiClient.get<YearlyStat[]>('/statistics/yearly')
  return data
}

export async function fetchByLift(): Promise<LiftStat[]> {
  const { data } = await apiClient.get<LiftStat[]>('/statistics/by-lift')
  return data
}

export async function fetchLiftStatDetail(liftId: number, year: number): Promise<LiftStatDetail> {
  const { data } = await apiClient.get<LiftStatDetail>(`/statistics/lifts/${liftId}`, {
    params: { year },
  })
  return data
}
