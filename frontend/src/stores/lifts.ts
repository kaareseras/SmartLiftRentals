import { defineStore } from 'pinia'
import { ref } from 'vue'

import { createLift, fetchLifts } from '../api/lifts'
import type { Lift, LiftCreate } from '../types/lift'

export const useLiftStore = defineStore('lifts', () => {
  const lifts = ref<Lift[]>([])
  const loading = ref(false)

  async function loadLifts(): Promise<void> {
    loading.value = true
    try {
      lifts.value = await fetchLifts()
    } finally {
      loading.value = false
    }
  }

  async function addLift(payload: LiftCreate): Promise<void> {
    const lift = await createLift(payload)
    lifts.value.push(lift)
  }

  return {
    lifts,
    loading,
    loadLifts,
    addLift,
  }
})
