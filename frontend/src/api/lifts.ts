import apiClient from './index'
import type { Lift, LiftCreate, LiftUpdate } from '../types/lift'

export async function fetchLifts(): Promise<Lift[]> {
  const { data } = await apiClient.get<Lift[]>('/lifts')
  return data
}

export async function fetchLift(id: number): Promise<Lift> {
  const { data } = await apiClient.get<Lift>(`/lifts/${id}`)
  return data
}

export async function createLift(payload: LiftCreate): Promise<Lift> {
  const { data } = await apiClient.post<Lift>('/lifts', payload)
  return data
}

export async function updateLift(id: number, payload: LiftUpdate): Promise<Lift> {
  const { data } = await apiClient.put<Lift>(`/lifts/${id}`, payload)
  return data
}

export async function deleteLift(id: number): Promise<void> {
  await apiClient.delete(`/lifts/${id}`)
}
