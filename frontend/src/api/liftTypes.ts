import apiClient from './index'
import type { LiftType, LiftTypeCreate, LiftTypeUpdate } from '../types/liftType'

export async function fetchLiftTypes(): Promise<LiftType[]> {
  const { data } = await apiClient.get<LiftType[]>('/lift-types')
  return data
}

export async function createLiftType(payload: LiftTypeCreate): Promise<LiftType> {
  const { data } = await apiClient.post<LiftType>('/lift-types', payload)
  return data
}

export async function updateLiftType(id: number, payload: LiftTypeUpdate): Promise<LiftType> {
  const { data } = await apiClient.put<LiftType>(`/lift-types/${id}`, payload)
  return data
}

export async function deleteLiftType(id: number): Promise<void> {
  await apiClient.delete(`/lift-types/${id}`)
}
