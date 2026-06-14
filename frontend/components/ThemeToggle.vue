<template>
  <button 
    @click="toggleTheme" 
    class="p-2 rounded-full bg-light-elevated dark:bg-dark-elevated text-light-muted dark:text-dark-muted hover:text-primary dark:hover:text-primary transition-colors focus:outline-none"
    aria-label="Toggle Theme"
  >
    <div ref="iconWrapper" class="flex items-center justify-center">
      <SunIcon v-if="isDark" class="h-5 w-5" />
      <MoonIcon v-else class="h-5 w-5" />
    </div>
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useColorMode } from '@vueuse/core';
import { SunIcon, MoonIcon } from '@heroicons/vue/24/outline';
import gsap from 'gsap';

const colorMode = useColorMode();
const iconWrapper = ref(null);

const isDark = ref(false);

onMounted(() => {
  isDark.value = colorMode.value === 'dark';
});

const toggleTheme = () => {
  const newMode = isDark.value ? 'light' : 'dark';
  colorMode.value = newMode;
  isDark.value = newMode === 'dark';
  
  if (iconWrapper.value) {
    gsap.fromTo(iconWrapper.value, 
      { rotation: 0, scale: 0.8 }, 
      { rotation: 360, scale: 1, duration: 0.4, ease: "back.out(1.7)" }
    );
  }
};
</script>
