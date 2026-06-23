export interface User {
  id: number
  name: string
  email: string
  is_active: boolean
  is_admin: boolean
  created_at: string
  updated_at: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface UserCreate {
  name: string
  email: string
  password: string
  is_admin?: boolean
}
