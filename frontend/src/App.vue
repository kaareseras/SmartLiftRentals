<template>
  <div v-if="isBare" class="bare-shell">
    <RouterView />
  </div>

  <div v-else class="app-shell">
    <header class="app-header">
      <div class="app-header__inner">
        <RouterLink to="/" class="brand">
          <span class="brand__mark" aria-hidden="true">SL</span>
          <span class="brand__name">SmartLiftRentals</span>
        </RouterLink>

        <nav class="app-nav">
          <RouterLink to="/" class="app-nav__link">Home</RouterLink>
          <RouterLink v-if="auth.isAuthenticated" to="/lifts" class="app-nav__link">
            Fleet
          </RouterLink>
          <RouterLink v-if="auth.isAdmin" to="/admin" class="app-nav__link">Admin</RouterLink>
        </nav>

        <div class="app-header__actions">
          <template v-if="auth.isAuthenticated">
            <div class="user-chip">
              <span class="user-chip__avatar">{{ initials }}</span>
              <span class="user-chip__meta">
                <span class="user-chip__name">{{ auth.user?.name }}</span>
                <span class="user-chip__role">{{ auth.isAdmin ? 'Administrator' : 'Operator' }}</span>
              </span>
            </div>
            <button class="btn btn-subtle btn-sm" @click="handleLogout">Sign out</button>
          </template>
          <RouterLink v-else to="/login" class="btn btn-primary btn-sm">Sign in</RouterLink>
        </div>
      </div>
    </header>

    <main class="app-main">
      <RouterView />
    </main>

    <footer class="app-footer">
      <span>© {{ year }} SmartLiftRentals</span>
      <span class="app-footer__dot">•</span>
      <span>IoT platform for construction lift rentals</span>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'

import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const year = new Date().getFullYear()

const isBare = computed(() => route.name === 'login')

const initials = computed(() => {
  const name = auth.user?.name?.trim() ?? ''
  if (!name) return 'U'
  return name
    .split(/\s+/)
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
})

onMounted(() => {
  if (auth.token && !auth.user) {
    void auth.fetchUser()
  }
})

async function handleLogout(): Promise<void> {
  auth.logout()
  await router.push('/')
}
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.bare-shell {
  min-height: 100vh;
}

/* ----- header ----- */
.app-header {
  position: sticky;
  top: 0;
  z-index: 50;
  height: var(--header-height);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border-strong);
  box-shadow: var(--shadow-sm);
}

.app-header__inner {
  max-width: var(--page-max);
  height: 100%;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  color: var(--color-heading);
}

.brand:hover {
  text-decoration: none;
}

.brand__mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent-deep));
  color: #fff;
  font-weight: 700;
  font-size: 0.8rem;
  letter-spacing: 0.02em;
}

.brand__name {
  font-weight: 600;
  font-size: 1rem;
}

.app-nav {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  height: 100%;
}

.app-nav__link {
  display: inline-flex;
  align-items: center;
  height: 100%;
  padding: 0 0.85rem;
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  border-bottom: 2px solid transparent;
}

.app-nav__link:hover {
  color: var(--color-heading);
  text-decoration: none;
}

.app-nav__link.router-link-exact-active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.app-header__actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}

.user-chip__avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-primary-soft);
  color: var(--color-primary-pressed);
  font-weight: 700;
  font-size: 0.78rem;
}

.user-chip__meta {
  display: flex;
  flex-direction: column;
  line-height: 1.15;
}

.user-chip__name {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--color-heading);
}

.user-chip__role {
  font-size: 0.72rem;
  color: var(--color-text-tertiary);
}

/* ----- main ----- */
.app-main {
  flex: 1;
}

/* ----- footer ----- */
.app-footer {
  border-top: 1px solid var(--color-border);
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  color: var(--color-text-tertiary);
  font-size: 0.8rem;
  background: var(--color-surface);
}

.app-footer__dot {
  opacity: 0.6;
}

@media (max-width: 640px) {
  .app-header__inner {
    gap: 1rem;
    padding: 0 1rem;
  }

  .brand__name {
    display: none;
  }

  .user-chip__meta {
    display: none;
  }
}
</style>
