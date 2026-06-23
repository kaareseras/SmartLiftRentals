import apiClient from './index'
import type { LiftTelemetry } from '../types/telemetry'

export async function fetchTelemetry(): Promise<LiftTelemetry[]> {
  const { data } = await apiClient.get<LiftTelemetry[]>('/telemetry')
  return data
}
