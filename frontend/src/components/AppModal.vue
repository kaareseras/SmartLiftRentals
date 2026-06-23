<template>
  <Teleport to="body">
    <div class="modal-backdrop" @click.self="emit('close')">
      <div class="modal card" role="dialog" aria-modal="true" :aria-label="title">
        <div class="modal__head">
          <h2 class="modal__title">{{ title }}</h2>
          <button type="button" class="modal__close" aria-label="Close" @click="emit('close')">
            &times;
          </button>
        </div>
        <slot />
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
defineProps<{ title: string }>()
const emit = defineEmits<{ (e: 'close'): void }>()
</script>
