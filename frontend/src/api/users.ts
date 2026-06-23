import apiClient from './index'
import type { User, UserCreate } from '../types/user'

export async function fetchUsers(): Promise<User[]> {
  const { data } = await apiClient.get<User[]>('/users')
  return data
}

export async function createUser(payload: UserCreate): Promise<User> {
  const { data } = await apiClient.post<User>('/users', payload)
  return data
}
