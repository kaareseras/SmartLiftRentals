<template>
  <section>
    <h2>Lifts</h2>

    <form class="lift-form" @submit.prevent="submit">
      <input v-model="form.uid" placeholder="UID" required />
      <input v-model="form.name" placeholder="Lift name" required />
      <input v-model="form.model" placeholder="Model" required />
      <button type="submit">Add lift</button>
    </form>

    <p v-if="store.loading">Loading lifts...</p>
    <ul v-else>
      <li v-for="lift in store.lifts" :key="lift.id">
        <strong>{{ lift.name }}</strong>
        <span>({{ lift.uid }}) - {{ lift.status }}</span>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import { onMounted, reactive } from 'vue'

import { useLiftStore } from '../stores/lifts'
import type { LiftCreate } from '../types/lift'

const store = useLiftStore()
const form = reactive<LiftCreate>({
  uid: '',
  name: '',
  model: '',
  status: 'available',
  location: null,
  latitude: null,
  longitude: null,
  last_seen: null,
})

async function submit(): Promise<void> {
  await store.addLift({ ...form })
  form.uid = ''
  form.name = ''
  form.model = ''
}

onMounted(() => {
  void store.loadLifts()
})
</script>

<style scoped>
.lift-form {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

button {
  cursor: pointer;
}

ul {
  padding-left: 1.25rem;
}
</style>
