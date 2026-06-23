<template>
  <div class="login">
    <!-- Brand panel -->
    <aside class="login__brand">
      <RouterLink to="/" class="login__brand-logo">
        <span class="login__brand-mark">SL</span>
        <span>SmartLiftRentals</span>
      </RouterLink>

      <div class="login__brand-body">
        <h1 class="login__brand-title">Operations console</h1>
        <p class="login__brand-text">
          Sign in to monitor live telemetry, manage your rental fleet, and administer the
          platform.
        </p>
        <ul class="login__brand-list">
          <li>Real-time MQTT telemetry</li>
          <li>Time-series utilisation insights</li>
          <li>Role-based administration</li>
        </ul>
      </div>

      <p class="login__brand-foot">© {{ year }} SmartLiftRentals</p>
    </aside>

    <!-- Form panel -->
    <main class="login__panel">
      <div class="login__card">
        <RouterLink to="/" class="login__back">← Back to home</RouterLink>
        <h2 class="login__title">Sign in</h2>
        <p class="login__subtitle">Use your platform account to continue.</p>

        <div v-if="auth.error" class="alert alert-error login__alert">{{ auth.error }}</div>

        <form @submit.prevent="handleLogin">
          <div class="field">
            <label class="label" for="email">Email</label>
            <input
              id="email"
              v-model="email"
              class="input"
              type="email"
              autocomplete="username"
              placeholder="you@example.com"
              required
              @input="auth.clearError()"
            />
          </div>

          <div class="field">
            <label class="label" for="password">Password</label>
            <input
              id="password"
              v-model="password"
              class="input"
              type="password"
              autocomplete="current-password"
              placeholder="Enter your password"
              required
              @input="auth.clearError()"
            />
          </div>

          <button class="btn btn-primary btn-block btn-lg login__submit" type="submit" :disabled="auth.loading">
            <span v-if="auth.loading" class="spinner login__spinner" />
            {{ auth.loading ? 'Signing in…' : 'Sign in' }}
          </button>
        </form>

        <div class="login__demo">
          <span class="login__demo-title">Demo administrator</span>
          <span class="mono">admin@smartliftrentals.com</span>
          <span class="mono">Admin123!</span>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const year = new Date().getFullYear()

const email = ref('')
const password = ref('')

function postLoginTarget(): string {
  const raw = route.query.redirect
  const candidate = Array.isArray(raw) ? raw[0] : raw
  if (typeof candidate === 'string' && candidate.startsWith('/') && !candidate.startsWith('//')) {
    return candidate
  }
  return auth.isAdmin ? '/admin' : '/lifts'
}

async function handleLogin(): Promise<void> {
  try {
    await auth.login(email.value, password.value)
    await router.push(postLoginTarget())
  } catch {
    // error surfaced via auth.error
  }
}
</script>

<style scoped>
.login {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1.05fr 1fr;
}

/* ----- brand panel ----- */
.login__brand {
  position: relative;
  color: #fff;
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(110% 110% at 80% 0%, rgba(43, 136, 216, 0.45) 0%, transparent 55%),
    linear-gradient(160deg, #0b3d68 0%, #004578 50%, #00243f 100%);
}

.login__brand-logo {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  color: #fff;
  font-weight: 600;
  font-size: 1.05rem;
  text-decoration: none;
}

.login__brand-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.16);
  font-weight: 700;
  font-size: 0.82rem;
}

.login__brand-body {
  margin: auto 0;
  max-width: 26rem;
}

.login__brand-title {
  color: #fff;
  font-size: 2.1rem;
  letter-spacing: -0.02em;
}

.login__brand-text {
  margin-top: 1rem;
  color: rgba(255, 255, 255, 0.82);
  font-size: 1rem;
  line-height: 1.6;
}

.login__brand-list {
  margin: 1.75rem 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.login__brand-list li {
  position: relative;
  padding-left: 1.6rem;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.92rem;
}

.login__brand-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.35rem;
  width: 14px;
  height: 8px;
  border-left: 2px solid #6dd58c;
  border-bottom: 2px solid #6dd58c;
  transform: rotate(-45deg);
}

.login__brand-foot {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
}

/* ----- form panel ----- */
.login__panel {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 1.5rem;
  background: var(--color-bg);
}

.login__card {
  width: 100%;
  max-width: 400px;
}

.login__back {
  display: inline-block;
  font-size: 0.82rem;
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
}

.login__title {
  font-size: 1.75rem;
  letter-spacing: -0.01em;
}

.login__subtitle {
  margin-top: 0.35rem;
  margin-bottom: 1.5rem;
  color: var(--color-text-secondary);
}

.login__alert {
  margin-bottom: 1.25rem;
}

.login__submit {
  margin-top: 0.5rem;
}

.login__spinner {
  width: 16px;
  height: 16px;
  border-width: 2px;
  border-top-color: #fff;
  border-color: rgba(255, 255, 255, 0.4);
  border-top-color: #fff;
}

.login__demo {
  margin-top: 1.75rem;
  padding: 0.9rem 1rem;
  border: 1px dashed var(--color-border-stronger);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  font-size: 0.82rem;
  color: var(--color-text-secondary);
}

.login__demo-title {
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 0.15rem;
}

@media (max-width: 860px) {
  .login {
    grid-template-columns: 1fr;
  }

  .login__brand {
    display: none;
  }
}
</style>
