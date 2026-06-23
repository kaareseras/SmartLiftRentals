import apiClient from './index'
import type { Cost, CostCreate, CostUpdate } from '../types/cost'

export async function fetchCosts(liftId?: number): Promise<Cost[]> {
  const { data } = await apiClient.get<Cost[]>('/costs', {
    params: liftId != null ? { lift_id: liftId } : undefined,
  })
  return data
}

export async function createCost(payload: CostCreate): Promise<Cost> {
  const { data } = await apiClient.post<Cost>('/costs', payload)
  return data
}

export async function updateCost(id: number, payload: CostUpdate): Promise<Cost> {
  const { data } = await apiClient.put<Cost>(`/costs/${id}`, payload)
  return data
}

export async function deleteCost(id: number): Promise<void> {
  await apiClient.delete(`/costs/${id}`)
}
