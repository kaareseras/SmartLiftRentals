import apiClient from './index'
import type { LoginResponse, User } from '../types/user'

export async function login(email: string, password: string): Promise<LoginResponse> {
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', password)

  const { data } = await apiClient.post<LoginResponse>('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return data
}

export async function fetchMe(): Promise<User> {
  const { data } = await apiClient.get<User>('/auth/me')
  return data
}
