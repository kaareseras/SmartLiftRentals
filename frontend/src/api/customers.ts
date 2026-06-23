import apiClient from './index'
import type { Customer, CustomerCreate, CustomerUpdate } from '../types/customer'

export async function fetchCustomers(): Promise<Customer[]> {
  const { data } = await apiClient.get<Customer[]>('/customers')
  return data
}

export async function createCustomer(payload: CustomerCreate): Promise<Customer> {
  const { data } = await apiClient.post<Customer>('/customers', payload)
  return data
}

export async function updateCustomer(id: number, payload: CustomerUpdate): Promise<Customer> {
  const { data } = await apiClient.put<Customer>(`/customers/${id}`, payload)
  return data
}

export async function deleteCustomer(id: number): Promise<void> {
  await apiClient.delete(`/customers/${id}`)
}
