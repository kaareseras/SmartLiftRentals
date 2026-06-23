<template>
  <div class="home">
    <!-- Hero -->
    <section class="hero">
      <div class="hero__inner">
        <div class="hero__content">
          <span class="hero__eyebrow">SmartLiftRentals Platform</span>
          <h1 class="hero__title">
            Connected intelligence for your<br />
            construction lift fleet
          </h1>
          <p class="hero__subtitle">
            Monitor live telemetry, track utilisation, and manage every rental asset from a
            single operations workspace — built on real-time MQTT, time-series data, and a
            secure role-based admin console.
          </p>
          <div class="hero__actions">
            <RouterLink :to="primaryCta.to" class="btn btn-primary btn-lg">
              {{ primaryCta.label }}
            </RouterLink>
            <RouterLink to="/lifts" class="btn btn-ghost-on-dark btn-lg">
              Explore the fleet
            </RouterLink>
          </div>
          <dl class="hero__stats">
            <div class="hero__stat">
              <dt>99.9%</dt>
              <dd>Telemetry uptime</dd>
            </div>
            <div class="hero__stat">
              <dt>&lt; 1s</dt>
              <dd>Live data latency</dd>
            </div>
            <div class="hero__stat">
              <dt>24/7</dt>
              <dd>Fleet visibility</dd>
            </div>
          </dl>
        </div>

        <!-- Product mock -->
        <div class="hero__visual" aria-hidden="true">
          <div class="mock">
            <div class="mock__bar">
              <span class="mock__dot" />
              <span class="mock__dot" />
              <span class="mock__dot" />
              <span class="mock__title">Fleet overview</span>
            </div>
            <div class="mock__body">
              <div class="mock__kpis">
                <div class="mock__kpi">
                  <span class="mock__kpi-value">128</span>
                  <span class="mock__kpi-label">Active lifts</span>
                </div>
                <div class="mock__kpi">
                  <span class="mock__kpi-value">12</span>
                  <span class="mock__kpi-label">In maintenance</span>
                </div>
                <div class="mock__kpi">
                  <span class="mock__kpi-value">96%</span>
                  <span class="mock__kpi-label">Utilisation</span>
                </div>
              </div>
              <div class="mock__list">
                <div v-for="row in mockRows" :key="row.uid" class="mock__row">
                  <span class="mock__row-name">{{ row.name }}</span>
                  <span class="mock__row-uid">{{ row.uid }}</span>
                  <span class="badge" :class="row.badge">{{ row.status }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="features page">
      <div class="features__head">
        <span class="page-eyebrow">Why SmartLiftRentals</span>
        <h2 class="features__title">Everything operations teams need in one place</h2>
      </div>
      <div class="features__grid">
        <article v-for="feature in features" :key="feature.title" class="card card-pad feature">
          <span class="feature__icon" v-html="feature.icon" />
          <h3 class="feature__title">{{ feature.title }}</h3>
          <p class="feature__text">{{ feature.text }}</p>
        </article>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta">
      <div class="cta__inner page">
        <div>
          <h2 class="cta__title">Ready to bring your fleet online?</h2>
          <p class="cta__text">
            Sign in to the operations console or talk to us about onboarding your rental
            inventory.
          </p>
        </div>
        <RouterLink :to="primaryCta.to" class="btn btn-primary btn-lg">
          {{ primaryCta.label }}
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()

const primaryCta = computed(() =>
  auth.isAuthenticated
    ? { to: auth.isAdmin ? '/admin' : '/lifts', label: 'Open console' }
    : { to: '/login', label: 'Sign in' },
)

const mockRows = [
  { uid: 'LFT-0481', name: 'Tower Crane North', status: 'Active', badge: 'badge-green' },
  { uid: 'LFT-0192', name: 'Hoist B12', status: 'Rented', badge: 'badge-blue' },
  { uid: 'LFT-0337', name: 'Mast Climber 4', status: 'Service', badge: 'badge-amber' },
  { uid: 'LFT-0508', name: 'Material Hoist 9', status: 'Active', badge: 'badge-green' },
]

const features = [
  {
    title: 'Real-time telemetry',
    text: 'Ingest lift health, location, and usage over MQTT and see it reflected on the dashboard within seconds.',
    icon: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l3 8 4-16 3 8h4"/></svg>',
  },
  {
    title: 'Fleet management',
    text: 'Register, update, and retire rental assets with a structured inventory and full status history.',
    icon: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
  },
  {
    title: 'Secure admin console',
    text: 'Role-based access keeps the admin workspace limited to authorised platform administrators.',
    icon: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/><path d="M9 12l2 2 4-4"/></svg>',
  },
]
</script>

<style scoped>
/* ----- hero ----- */
.hero {
  background:
    radial-gradient(120% 120% at 85% 0%, rgba(43, 136, 216, 0.45) 0%, transparent 55%),
    linear-gradient(135deg, #0b3d68 0%, #004578 45%, #00243f 100%);
  color: #fff;
  overflow: hidden;
}

.hero__inner {
  max-width: var(--page-max);
  margin: 0 auto;
  padding: 4.5rem 1.5rem 4rem;
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 3rem;
  align-items: center;
}

.hero__eyebrow {
  display: inline-block;
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #9ad0ff;
  margin-bottom: 1rem;
}

.hero__title {
  color: #fff;
  font-size: 2.75rem;
  line-height: 1.1;
  letter-spacing: -0.02em;
  font-weight: 700;
}

.hero__subtitle {
  margin-top: 1.25rem;
  max-width: 38rem;
  color: rgba(255, 255, 255, 0.82);
  font-size: 1.05rem;
  line-height: 1.6;
}

.hero__actions {
  margin-top: 2rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
}

.hero__stats {
  margin: 2.75rem 0 0;
  display: flex;
  gap: 2.5rem;
}

.hero__stat dt {
  font-size: 1.6rem;
  font-weight: 700;
  color: #fff;
}

.hero__stat dd {
  margin: 0.15rem 0 0;
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.7);
}

/* ----- hero mock ----- */
.hero__visual {
  perspective: 1600px;
}

.mock {
  background: var(--color-surface);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  transform: rotateY(-8deg) rotateX(3deg);
  transform-origin: center;
}

.mock__bar {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.7rem 0.9rem;
  background: var(--color-bg-alt);
  border-bottom: 1px solid var(--color-border);
}

.mock__dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--color-border-stronger);
}

.mock__title {
  margin-left: 0.5rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.mock__body {
  padding: 1.1rem;
}

.mock__kpis {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.6rem;
  margin-bottom: 1rem;
}

.mock__kpi {
  background: var(--color-primary-tint);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 0.7rem;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.mock__kpi-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-primary-pressed);
}

.mock__kpi-label {
  font-size: 0.68rem;
  color: var(--color-text-secondary);
}

.mock__list {
  display: flex;
  flex-direction: column;
}

.mock__row {
  display: grid;
  grid-template-columns: 1fr auto auto;
  align-items: center;
  gap: 0.6rem;
  padding: 0.6rem 0.25rem;
  border-bottom: 1px solid var(--color-border);
}

.mock__row:last-child {
  border-bottom: none;
}

.mock__row-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--color-heading);
}

.mock__row-uid {
  font-size: 0.74rem;
  color: var(--color-text-tertiary);
  font-family: 'Cascadia Code', 'Consolas', monospace;
}

/* ----- features ----- */
.features__head {
  text-align: center;
  margin-bottom: 2rem;
}

.features__title {
  font-size: 1.75rem;
  letter-spacing: -0.01em;
}

.features__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}

.feature__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background: var(--color-primary-soft);
  color: var(--color-primary-pressed);
  margin-bottom: 1rem;
}

.feature__title {
  font-size: 1.1rem;
  margin-bottom: 0.4rem;
}

.feature__text {
  color: var(--color-text-secondary);
  font-size: 0.9rem;
  line-height: 1.55;
}

/* ----- cta ----- */
.cta {
  background: var(--color-bg-alt);
  border-top: 1px solid var(--color-border);
}

.cta__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.cta__title {
  font-size: 1.5rem;
}

.cta__text {
  margin-top: 0.4rem;
  color: var(--color-text-secondary);
  max-width: 36rem;
}

@media (max-width: 900px) {
  .hero__inner {
    grid-template-columns: 1fr;
    padding: 3rem 1.5rem;
  }

  .hero__visual {
    order: -1;
  }

  .mock {
    transform: none;
  }

  .features__grid {
    grid-template-columns: 1fr;
  }

  .hero__title {
    font-size: 2.1rem;
  }
}

@media (max-width: 560px) {
  .hero__stats {
    gap: 1.5rem;
  }
}
</style>
