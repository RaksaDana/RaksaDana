<template>
  <aside class="w-[260px] flex-shrink-0 bg-light-surface dark:bg-dark-surface border-r border-light-border dark:border-dark-border flex flex-col h-screen sticky top-0 transition-colors duration-300 shadow-sm dark:shadow-none">
    <!-- Logo area -->
    <div class="p-6 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <img ref="logoRef" src="/logo.png" alt="RaksaDana Logo" class="h-10 w-10 opacity-0" />
        <div>
          <h1 class="text-[18px] font-bold tracking-tight text-light-text dark:text-dark-text">RaksaDana</h1>
          <p class="text-[12px] text-light-muted dark:text-dark-muted">Platform Investasi Saham AI</p>
        </div>
      </div>
      <!-- Theme Toggle inside sidebar -->
      <ThemeToggle />
    </div>
    
    <div class="px-6 pb-4">
      <div class="h-px w-full bg-light-border dark:bg-dark-border"></div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 px-4 space-y-2">
      <NuxtLink 
        to="/" 
        class="flex items-center gap-3 px-4 py-3 rounded-lg text-light-muted dark:text-dark-muted hover:bg-light-elevated dark:hover:bg-dark-elevated hover:text-light-text dark:hover:text-dark-text transition-colors duration-200"
        active-class="bg-primary/10 border-l-4 border-primary text-primary hover:bg-primary/10 hover:text-primary !pl-3"
      >
        <HomeIcon class="h-5 w-5" />
        <span class="text-[14px] font-medium">Dashboard</span>
      </NuxtLink>
      <NuxtLink 
        to="/kalkulator" 
        class="flex items-center gap-3 px-4 py-3 rounded-lg text-light-muted dark:text-dark-muted hover:bg-light-elevated dark:hover:bg-dark-elevated hover:text-light-text dark:hover:text-dark-text transition-colors duration-200"
        active-class="bg-primary/10 border-l-4 border-primary text-primary hover:bg-primary/10 hover:text-primary !pl-3"
      >
        <CalculatorIcon class="h-5 w-5" />
        <span class="text-[14px] font-medium">Kalkulator</span>
      </NuxtLink>
    </nav>

    <!-- Disclaimer -->
    <div class="p-6 mt-auto">
      <p class="text-[11px] text-light-muted dark:text-dark-muted leading-relaxed text-center">
        Data bersumber dari model prediksi AI. Bukan merupakan saran investasi resmi.
      </p>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { HomeIcon, CalculatorIcon } from '@heroicons/vue/24/outline';
import ThemeToggle from './ThemeToggle.vue';
import gsap from 'gsap';

const logoRef = ref(null);

onMounted(() => {
  if (logoRef.value) {
    gsap.fromTo(logoRef.value, 
      { opacity: 0, scale: 1 },
      { opacity: 1, scale: 1.05, duration: 0.6, ease: "power2.out" }
    );
  }
});
</script>
