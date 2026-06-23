import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { fetchMe, login as loginRequest } from '../api/auth'
import { getToken, setToken } from '../api'
import type { User } from '../types/user'

function extractError(error: unknown, fallback: string): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail
    if (typeof detail === 'string') return detail
  }
  return fallback
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(getToken())
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin ?? false)

  function clearError(): void {
    error.value = null
  }

  async function login(email: string, password: string): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const result = await loginRequest(email, password)
      token.value = result.access_token
      setToken(result.access_token)
      user.value = result.user
    } catch (e) {
      error.value = extractError(e, 'Unable to sign in. Please check your credentials.')
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchUser(): Promise<void> {
    if (!token.value) return
    try {
      user.value = await fetchMe()
    } catch {
      user.value = null
      token.value = null
      setToken(null)
    }
  }

  function logout(): void {
    user.value = null
    token.value = null
    setToken(null)
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    clearError,
    login,
    fetchUser,
    logout,
  }
})
