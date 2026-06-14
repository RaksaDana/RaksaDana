<template>
  <div class="glass-card rounded-2xl p-6 border-l-[3px] border-l-purple shadow-md h-full">
    <div class="flex items-center gap-3 mb-4">
      <SparklesIcon class="h-6 w-6 text-purple" />
      <h3 class="text-[16px] font-semibold text-light-text dark:text-dark-text">Analisis AI</h3>
      <span class="px-2 py-0.5 rounded-full bg-gradient-to-r from-primary to-purple text-[10px] text-white font-medium shadow-sm">Gemini AI</span>
    </div>
    
    <div v-if="loading" class="space-y-3">
      <SkeletonLoader customClass="h-4 w-full" />
      <SkeletonLoader customClass="h-4 w-11/12" />
      <SkeletonLoader customClass="h-4 w-4/5" />
    </div>
    <div v-else-if="error || !narration" class="text-[14px] text-light-muted dark:text-dark-muted italic">
      Analisis AI tidak tersedia saat ini.
    </div>
    <div v-else class="text-[14px] text-light-text dark:text-dark-text leading-[1.8] whitespace-pre-wrap">
      {{ displayedText }}<span v-if="isTyping" class="animate-pulse text-primary">|</span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { SparklesIcon } from '@heroicons/vue/24/solid';
import SkeletonLoader from './SkeletonLoader.vue';

const props = defineProps({
  narration: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: [Boolean, String],
    default: false
  }
});

const displayedText = ref('');
const isTyping = ref(false);
let typingTimer = null;

const typeWriter = (text) => {
  if (typingTimer) clearInterval(typingTimer);
  displayedText.value = '';
  isTyping.value = true;
  let i = 0;
  
  typingTimer = setInterval(() => {
    if (i < text.length) {
      displayedText.value += text.charAt(i);
      i++;
    } else {
      clearInterval(typingTimer);
      isTyping.value = false;
    }
  }, 15);
};

onMounted(() => {
  if (props.narration && !props.loading && !props.error) {
    typeWriter(props.narration);
  }
});

watch(() => props.narration, (newVal) => {
  if (newVal && !props.loading && !props.error) {
    typeWriter(newVal);
  }
});

onUnmounted(() => {
  if (typingTimer) clearInterval(typingTimer);
});
</script>
