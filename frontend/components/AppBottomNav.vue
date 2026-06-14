<template>
  <nav class="fixed bottom-0 left-0 right-0 z-50 px-6 py-2 flex justify-around items-center pb-safe glass-surface rounded-t-2xl">
    <NuxtLink 
      to="/" 
      class="flex flex-col items-center gap-1 p-2 text-light-muted dark:text-dark-muted transition-colors duration-200 relative"
      active-class="text-primary dark:text-primary"
    >
      <HomeIcon class="h-6 w-6" />
      <span class="text-[11px] font-medium">Dashboard</span>
      <div class="absolute top-0 w-8 h-[2px] bg-primary rounded-full opacity-0 transition-opacity" :class="$route.path === '/' ? 'opacity-100' : ''"></div>
    </NuxtLink>
    <NuxtLink 
      to="/kalkulator" 
      class="flex flex-col items-center gap-1 p-2 text-light-muted dark:text-dark-muted transition-colors duration-200 relative"
      active-class="text-primary dark:text-primary"
    >
      <CalculatorIcon class="h-6 w-6" />
      <span class="text-[11px] font-medium">Kalkulator</span>
      <div class="absolute top-0 w-8 h-[2px] bg-primary rounded-full opacity-0 transition-opacity" :class="$route.path === '/kalkulator' ? 'opacity-100' : ''"></div>
    </NuxtLink>
  </nav>
</template>

<script setup>
import { HomeIcon, CalculatorIcon } from '@heroicons/vue/24/outline';
import { useRoute } from 'vue-router';

const $route = useRoute();
</script>
<style scoped>
.pb-safe {
  padding-bottom: env(safe-area-inset-bottom, 0.5rem);
}
</style>
