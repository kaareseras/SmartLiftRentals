<template>
  <div class="page admin-users">
    <RouterLink to="/admin" class="back-link">← Admin console</RouterLink>

    <header class="page-header admin-users__header">
      <div>
        <h1 class="page-title">User management</h1>
        <p class="page-subtitle">{{ users.length }} total accounts</p>
      </div>
      <button class="btn btn-primary" @click="openCreate">+ New user</button>
    </header>

    <!-- Toolbar -->
    <div class="toolbar card card-pad">
      <input
        v-model="search"
        class="input toolbar__search"
        type="search"
        placeholder="Search by name or email…"
      />
      <select v-model="roleFilter" class="select toolbar__filter">
        <option value="all">All roles</option>
        <option value="admin">Administrators</option>
        <option value="user">Operators</option>
      </select>
      <button class="btn btn-secondary" :disabled="loading" @click="load">
        {{ loading ? 'Refreshing…' : 'Refresh' }}
      </button>
    </div>

    <div v-if="error" class="alert alert-error admin-users__alert">{{ error }}</div>

    <!-- States -->
    <div v-if="loading" class="state card">
      <span class="spinner" />
      <p>Loading users…</p>
    </div>

    <div v-else-if="filteredUsers.length === 0" class="state card">
      <p>No users match your filters.</p>
    </div>

    <!-- Table -->
    <div v-else class="card admin-users__table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Joined</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>
              <div class="cell-user">
                <span class="cell-user__avatar">{{ initialsOf(user.name) }}</span>
                <span class="cell-user__name">{{ user.name }}</span>
              </div>
            </td>
            <td class="cell-email">{{ user.email }}</td>
            <td>
              <span class="badge" :class="user.is_admin ? 'badge-blue' : 'badge-gray'">
                {{ user.is_admin ? 'Administrator' : 'Operator' }}
              </span>
            </td>
            <td>
              <span class="badge" :class="user.is_active ? 'badge-green' : 'badge-gray'">
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="cell-date">{{ formatDate(user.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create user modal -->
    <div v-if="showCreate" class="modal-backdrop" @click.self="closeCreate">
      <div class="modal card" role="dialog" aria-modal="true" aria-label="Create user">
        <h2 class="modal__title">Create user</h2>
        <p class="modal__subtitle">Add a new account to the platform.</p>

        <div v-if="createError" class="alert alert-error modal__alert">{{ createError }}</div>

        <form @submit.prevent="submitCreate">
          <div class="field">
            <label class="label" for="new-name">Full name</label>
            <input id="new-name" v-model="form.name" class="input" type="text" required />
          </div>
          <div class="field">
            <label class="label" for="new-email">Email</label>
            <input id="new-email" v-model="form.email" class="input" type="email" required />
          </div>
          <div class="field">
            <label class="label" for="new-password">Password</label>
            <input
              id="new-password"
              v-model="form.password"
              class="input"
              type="password"
              minlength="8"
              required
            />
            <span class="field-hint">At least 8 characters.</span>
          </div>
          <label class="checkbox">
            <input v-model="form.is_admin" type="checkbox" />
            <span>Grant administrator access</span>
          </label>

          <div class="modal__actions">
            <button type="button" class="btn btn-secondary" @click="closeCreate">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="creating">
              <span v-if="creating" class="spinner modal__spinner" />
              {{ creating ? 'Creating…' : 'Create user' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'

import { createUser, fetchUsers } from '../../api/users'
import type { User, UserCreate } from '../../types/user'

const users = ref<User[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const search = ref('')
const roleFilter = ref<'all' | 'admin' | 'user'>('all')

const showCreate = ref(false)
const creating = ref(false)
const createError = ref<string | null>(null)
const form = reactive<UserCreate>({ name: '', email: '', password: '', is_admin: false })

const filteredUsers = computed(() => {
  const query = search.value.trim().toLowerCase()
  return users.value.filter((user) => {
    if (roleFilter.value === 'admin' && !user.is_admin) return false
    if (roleFilter.value === 'user' && user.is_admin) return false
    if (query && !user.name.toLowerCase().includes(query) && !user.email.toLowerCase().includes(query)) {
      return false
    }
    return true
  })
})

function initialsOf(name: string): string {
  return (
    name
      .trim()
      .split(/\s+/)
      .map((part) => part[0])
      .slice(0, 2)
      .join('')
      .toUpperCase() || 'U'
  )
}

function formatDate(value: string): string {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    users.value = await fetchUsers()
  } catch (e) {
    error.value = axios.isAxiosError(e)
      ? (e.response?.data?.detail ?? 'Failed to load users.')
      : 'Failed to load users.'
  } finally {
    loading.value = false
  }
}

function openCreate(): void {
  form.name = ''
  form.email = ''
  form.password = ''
  form.is_admin = false
  createError.value = null
  showCreate.value = true
}

function closeCreate(): void {
  showCreate.value = false
}

async function submitCreate(): Promise<void> {
  creating.value = true
  createError.value = null
  try {
    const created = await createUser({ ...form })
    users.value.push(created)
    showCreate.value = false
  } catch (e) {
    createError.value = axios.isAxiosError(e)
      ? (e.response?.data?.detail ?? 'Failed to create user.')
      : 'Failed to create user.'
  } finally {
    creating.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.back-link {
  display: inline-block;
  font-size: 0.82rem;
  color: var(--color-text-secondary);
  margin-bottom: 0.75rem;
}

.admin-users__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.toolbar {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-bottom: 1.25rem;
  padding: 0.85rem 1rem;
}

.toolbar__search {
  flex: 1 1 auto;
}

.toolbar__filter {
  width: auto;
  min-width: 180px;
}

.admin-users__alert {
  margin-bottom: 1.25rem;
}

.admin-users__table-wrap {
  overflow: hidden;
}

.state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.cell-user {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.cell-user__avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--color-primary-soft);
  color: var(--color-primary-pressed);
  font-weight: 700;
  font-size: 0.72rem;
  flex-shrink: 0;
}

.cell-user__name {
  font-weight: 600;
  color: var(--color-heading);
}

.cell-email {
  color: var(--color-text-secondary);
}

.cell-date {
  color: var(--color-text-secondary);
  white-space: nowrap;
}

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  z-index: 100;
}

.modal {
  width: 100%;
  max-width: 440px;
  padding: 1.75rem;
  box-shadow: var(--shadow-xl);
}

.modal__title {
  font-size: 1.3rem;
}

.modal__subtitle {
  margin-top: 0.25rem;
  margin-bottom: 1.25rem;
  color: var(--color-text-secondary);
  font-size: 0.9rem;
}

.modal__alert {
  margin-bottom: 1rem;
}

.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.88rem;
  color: var(--color-text);
  margin-top: 0.25rem;
}

.modal__actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.modal__spinner {
  width: 14px;
  height: 14px;
  border-width: 2px;
  border-top-color: #fff;
  border-color: rgba(255, 255, 255, 0.4);
  border-top-color: #fff;
}

@media (max-width: 640px) {
  .toolbar {
    flex-wrap: wrap;
  }

  .toolbar__filter {
    flex: 1 1 auto;
  }
}
</style>
