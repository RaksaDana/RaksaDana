<template>
  <div class="glass-card rounded-2xl p-6 border-l-[3px] border-l-purple shadow-md h-full flex flex-col">
    <div class="flex items-center gap-3 mb-4">
      <SparklesIcon class="h-6 w-6 text-purple" />
      <h3 class="text-[16px] font-semibold text-light-text dark:text-dark-text">Analisis AI</h3>
      <span class="px-2 py-0.5 rounded-full bg-gradient-to-r from-primary to-purple text-[10px] text-white font-medium shadow-sm">Gemini AI</span>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="space-y-3">
      <SkeletonBlock width="100%" height="16px" borderRadius="4px" />
      <SkeletonBlock width="80%" height="16px" borderRadius="4px" />
      <SkeletonBlock width="60%" height="16px" borderRadius="4px" />
      <div class="mt-4 flex justify-center">
        <button disabled class="border border-primary/50 text-primary/50 px-4 py-2 rounded-lg text-[14px] font-medium flex items-center justify-center gap-2 w-full cursor-not-allowed">
          <div class="w-4 h-4 border-2 border-primary/30 border-t-primary rounded-full animate-spin"></div>
          Sedang menganalisis...
        </button>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-danger/10 border-l-[3px] border-danger rounded-r-xl p-4 flex flex-col gap-3">
      <div class="flex items-start gap-2">
        <ExclamationTriangleIcon class="w-5 h-5 text-danger shrink-0 mt-0.5" />
        <span class="text-[14px] text-danger font-medium">{{ typeof error === 'string' ? error : 'Analisis AI tidak tersedia saat ini. Coba beberapa saat lagi.' }}</span>
      </div>
      <button @click="$emit('request')" class="text-[12px] font-semibold text-danger underline w-fit hover:opacity-80">Coba Lagi</button>
    </div>

    <!-- Default State (No Narration yet) -->
    <div v-else-if="!narration" class="flex flex-col items-center justify-center py-6 text-center h-full gap-4">
      <p class="text-[14px] text-light-muted dark:text-dark-muted">Klik tombol di bawah untuk mendapatkan analisis AI</p>
      <button 
        @click="$emit('request')" 
        class="border border-primary text-primary hover:bg-primary/10 transition-colors px-4 py-2 rounded-lg text-[14px] font-medium flex items-center justify-center w-full"
      >
        {{ buttonText }}
      </button>
    </div>

    <!-- Narration Result -->
    <div v-else class="flex flex-col h-full">
      <div class="text-[14px] text-light-text dark:text-dark-text leading-[1.8] whitespace-pre-wrap flex-1">
        {{ displayedText }}<span v-if="isTyping" class="animate-pulse text-primary">|</span>
      </div>
      
      <div v-if="!isTyping" class="mt-4 pt-3 border-t border-light-border dark:border-dark-border">
        <button @click="$emit('request')" class="text-[12px] text-primary hover:underline font-medium">
          Refresh Analisis
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { SparklesIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline';
import SkeletonBlock from './SkeletonBlock.vue';

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
  },
  buttonText: {
    type: String,
    default: 'Analisis dengan AI'
  }
});

defineEmits(['request']);

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
  }, 20); // changed to 20ms as requested
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
