<template>
  <div class="particles-container">
    <div v-for="i in 8" :key="i" class="particle"></div>
  </div>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup>
import { useColorMode } from '@vueuse/core';
useColorMode(); // Initialize color mode to update HTML class
</script>

<style>
.page-enter-active,
.page-leave-active {
  transition: all 0.2s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateX(20px);
}
.page-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
