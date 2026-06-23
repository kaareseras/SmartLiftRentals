import apiClient from './index'
import type { Contract, ContractCreate, ContractUpdate } from '../types/contract'

export async function fetchContracts(liftId?: number): Promise<Contract[]> {
  const { data } = await apiClient.get<Contract[]>('/contracts', {
    params: liftId != null ? { lift_id: liftId } : undefined,
  })
  return data
}

export async function createContract(payload: ContractCreate): Promise<Contract> {
  const { data } = await apiClient.post<Contract>('/contracts', payload)
  return data
}

export async function updateContract(id: number, payload: ContractUpdate): Promise<Contract> {
  const { data } = await apiClient.put<Contract>(`/contracts/${id}`, payload)
  return data
}

export async function deleteContract(id: number): Promise<void> {
  await apiClient.delete(`/contracts/${id}`)
}
