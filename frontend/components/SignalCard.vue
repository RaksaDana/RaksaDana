<template>
  <div class="glass-card rounded-2xl p-[2px] transform transition-all duration-200">
    <!-- Loading State -->
    <div v-if="loading" class="relative bg-light-surface dark:bg-dark-surface/90 rounded-2xl p-6 h-[192px] flex flex-col justify-between">
      <SkeletonBlock width="80px" height="24px" borderRadius="16px" />
      <div class="grid grid-cols-2 gap-4">
        <div>
          <SkeletonBlock width="100px" height="14px" borderRadius="4px" class="mb-2" />
          <SkeletonBlock width="150px" height="36px" borderRadius="4px" />
        </div>
        <div class="flex flex-col items-end">
          <SkeletonBlock width="100px" height="14px" borderRadius="4px" class="mb-2" />
          <SkeletonBlock width="150px" height="36px" borderRadius="4px" />
        </div>
      </div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="relative bg-danger/10 border-l-[3px] border-danger rounded-xl p-6 h-[192px] flex flex-col justify-center gap-4 m-0.5">
      <div class="flex items-start gap-2">
        <ExclamationTriangleIcon class="w-6 h-6 text-danger shrink-0 mt-0.5" />
        <span class="text-[16px] text-danger font-medium">{{ typeof error === 'string' ? error : 'Gagal memuat sinyal prediksi.' }}</span>
      </div>
      <button @click="$emit('retry')" class="text-[14px] font-semibold text-danger underline w-fit hover:opacity-80">Coba Lagi</button>
    </div>

    <!-- Ready State -->
    <div v-else-if="prediction" class="h-full">
      <div :class="['absolute inset-0 rounded-2xl opacity-20 dark:opacity-40', gradientClass]"></div>
      <div class="relative bg-light-surface dark:bg-dark-surface/90 rounded-2xl p-6 h-[192px] flex flex-col gap-6 backdrop-blur-md">
        <div class="flex justify-between items-start">
          <div :class="['px-4 py-1.5 rounded-full text-[12px] font-bold uppercase tracking-wider shadow-lg', badgeClass, pulseClass]">
            {{ signalText }}
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-[12px] text-light-muted dark:text-dark-muted mb-1">Harga Penutupan</p>
            <h2 class="text-[32px] font-bold text-light-text dark:text-dark-text tracking-tight">{{ formatShortCurrency(displayBaseClose) }}</h2>
            <p class="text-[12px] text-light-muted dark:text-dark-muted mt-1">{{ formatDate(prediction.signal_date) }}</p>
          </div>
          
          <div class="text-right">
            <p class="text-[12px] text-light-muted dark:text-dark-muted mb-1">Prediksi Besok</p>
            <h2 :class="['text-[32px] font-bold tracking-tight', textClass]">{{ formatShortCurrency(displayPredictedClose) }}</h2>
            <p :class="['text-[12px] mt-1 font-medium flex items-center justify-end gap-1', returnClass]">
              <component :is="returnIcon" class="w-3 h-3" />
              {{ returnText }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { formatShortCurrency, formatDate } from '~/utils/formatters';
import { ArrowUpIcon, ArrowDownIcon, MinusIcon } from '@heroicons/vue/24/solid';
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline';
import SkeletonBlock from './SkeletonBlock.vue';
import gsap from 'gsap';

const props = defineProps({
  prediction: {
    type: Object,
    default: null
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

defineEmits(['retry']);

const isBuy = computed(() => props.prediction?.signal === 'BUY');
const isSell = computed(() => props.prediction?.signal === 'SELL');

const signalText = computed(() => {
  if (isBuy.value) return 'BELI';
  if (isSell.value) return 'JUAL';
  return 'TAHAN';
});

const gradientClass = computed(() => {
  if (isBuy.value) return 'bg-gradient-to-r from-primary to-success';
  if (isSell.value) return 'bg-gradient-to-r from-primary to-danger';
  return 'bg-gradient-to-r from-primary to-warning';
});

const badgeClass = computed(() => {
  if (isBuy.value) return 'bg-success text-white';
  if (isSell.value) return 'bg-danger text-white';
  return 'bg-warning text-white';
});

const pulseClass = computed(() => {
  if (isBuy.value) return 'animate-glow-success';
  if (isSell.value) return 'animate-glow-danger';
  return 'animate-glow-warning';
});

const textClass = computed(() => {
  if (isBuy.value) return 'text-success';
  if (isSell.value) return 'text-danger';
  return 'text-warning';
});

const returnText = computed(() => {
  const ret = props.prediction?.predicted_log_return;
  if (!ret) return '';
  const val = Math.abs(ret * 100);
  return `${val.toFixed(2).replace('.', ',')}%`;
});

const returnClass = computed(() => {
  const ret = props.prediction?.predicted_log_return;
  if (ret > 0) return 'text-success';
  if (ret < 0) return 'text-danger';
  return 'text-light-muted dark:text-dark-muted';
});

const returnIcon = computed(() => {
  const ret = props.prediction?.predicted_log_return;
  if (ret > 0) return ArrowUpIcon;
  if (ret < 0) return ArrowDownIcon;
  return MinusIcon;
});

// GSAP Counters
const displayBaseClose = ref(0);
const displayPredictedClose = ref(0);

const animateCounters = () => {
  if (props.prediction) {
    gsap.to(displayBaseClose, { value: props.prediction.base_close || 0, duration: 0.8, ease: 'power2.out' });
    gsap.to(displayPredictedClose, { value: props.prediction.predicted_close || 0, duration: 0.8, ease: 'power2.out' });
  }
};

onMounted(() => {
  animateCounters();
});

watch(() => props.prediction, () => {
  displayBaseClose.value = 0;
  displayPredictedClose.value = 0;
  animateCounters();
}, { deep: true });
</script>
