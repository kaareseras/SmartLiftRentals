<template>
  <div class="app-shell">
    <header>
      <h1>SmartLiftRentals</h1>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/lifts">Lifts</RouterLink>
      </nav>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
.app-shell {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: Arial, sans-serif;
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

nav {
  display: flex;
  gap: 1rem;
}

a {
  color: #2563eb;
  text-decoration: none;
}

.router-link-active {
  font-weight: 700;
}
</style>
