<template>
  <div class="relative min-h-[120px]">
    <!-- Loading State -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <SkeletonBlock v-for="i in 4" :key="i" width="100%" height="120px" borderRadius="12px" />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-danger/10 border-l-[3px] border-danger rounded-xl p-6 flex flex-col justify-center gap-3 w-full">
      <div class="flex items-start gap-2">
        <ExclamationTriangleIcon class="w-6 h-6 text-danger shrink-0 mt-0.5" />
        <span class="text-[16px] text-danger font-medium">{{ typeof error === 'string' ? error : 'Gagal memuat metrik model.' }}</span>
      </div>
      <button @click="$emit('retry')" class="text-[14px] font-semibold text-danger underline w-fit hover:opacity-80">Coba Lagi</button>
    </div>

    <!-- Ready State -->
    <div v-else-if="metrics" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" ref="gridRef">
      <!-- MAPE -->
      <div class="metric-card glass-card rounded-xl p-4 hover:-translate-y-1 hover:shadow-[0_0_15px_rgba(59,130,246,0.15)] transition-all duration-200">
        <div class="flex flex-col gap-2">
          <div class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
            <ChartBarIcon class="h-5 w-5 text-primary" />
          </div>
          <p class="text-[11px] uppercase text-light-muted dark:text-dark-muted font-semibold tracking-wider mt-2">MAPE</p>
          <h3 class="text-[28px] font-bold text-light-text dark:text-dark-text">{{ displayMape.toFixed(2).replace('.', ',') }}<span class="text-[16px] text-light-muted dark:text-dark-muted" v-if="metrics?.mape !== undefined">%</span></h3>
          <p class="text-[12px] text-light-muted dark:text-dark-muted">Rata-rata persentase kesalahan prediksi harga</p>
        </div>
      </div>
      
      <!-- R2 -->
      <div class="metric-card glass-card rounded-xl p-4 hover:-translate-y-1 hover:shadow-[0_0_15px_rgba(16,185,129,0.15)] transition-all duration-200">
        <div class="flex flex-col gap-2">
          <div class="w-10 h-10 rounded-full bg-emerald-500/10 flex items-center justify-center">
            <CheckBadgeIcon class="h-5 w-5 text-emerald-500" />
          </div>
          <p class="text-[11px] uppercase text-light-muted dark:text-dark-muted font-semibold tracking-wider mt-2">R²</p>
          <h3 class="text-[28px] font-bold text-light-text dark:text-dark-text">{{ displayR2.toFixed(4).replace('.', ',') }}</h3>
          <p class="text-[12px] text-light-muted dark:text-dark-muted">Seberapa baik model menjelaskan variasi harga (0-1)</p>
        </div>
      </div>
      
      <!-- Akurasi Arah -->
      <div class="metric-card glass-card rounded-xl p-4 hover:-translate-y-1 hover:shadow-[0_0_15px_rgba(245,158,11,0.15)] transition-all duration-200">
        <div class="flex flex-col gap-2">
          <div class="w-10 h-10 rounded-full bg-amber-500/10 flex items-center justify-center">
            <ArrowTrendingUpIcon class="h-5 w-5 text-amber-500" />
          </div>
          <p class="text-[11px] uppercase text-light-muted dark:text-dark-muted font-semibold tracking-wider mt-2">Akurasi Arah</p>
          <h3 class="text-[28px] font-bold text-light-text dark:text-dark-text">{{ displayAcc.toFixed(2).replace('.', ',') }}<span class="text-[16px] text-light-muted dark:text-dark-muted" v-if="metrics?.direction_accuracy !== undefined">%</span></h3>
          <p class="text-[12px] text-light-muted dark:text-dark-muted">Persentase prediksi arah naik/turun yang benar</p>
        </div>
      </div>
      
      <!-- Return RMSE -->
      <div class="metric-card glass-card rounded-xl p-4 hover:-translate-y-1 hover:shadow-[0_0_15px_rgba(139,92,246,0.15)] transition-all duration-200">
        <div class="flex flex-col gap-2">
          <div class="w-10 h-10 rounded-full bg-purple/10 flex items-center justify-center">
            <CalculatorIcon class="h-5 w-5 text-purple" />
          </div>
          <p class="text-[11px] uppercase text-light-muted dark:text-dark-muted font-semibold tracking-wider mt-2">Return RMSE</p>
          <h3 class="text-[28px] font-bold text-light-text dark:text-dark-text">{{ displayRmse.toFixed(6).replace('.', ',') }}</h3>
          <p class="text-[12px] text-light-muted dark:text-dark-muted">Kesalahan akar rata-rata kuadrat imbal hasil</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { ChartBarIcon, CheckBadgeIcon, ArrowTrendingUpIcon, CalculatorIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline';
import SkeletonBlock from './SkeletonBlock.vue';
import gsap from 'gsap';

const props = defineProps({
  metrics: {
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

const gridRef = ref(null);

const displayMape = ref(0);
const displayR2 = ref(0);
const displayAcc = ref(0);
const displayRmse = ref(0);

const animateCounters = () => {
  gsap.to(displayMape, { value: props.metrics?.mape || 0, duration: 0.8, ease: 'power2.out' });
  gsap.to(displayR2, { value: props.metrics?.r2 || 0, duration: 0.8, ease: 'power2.out' });
  gsap.to(displayAcc, { value: props.metrics?.direction_accuracy || 0, duration: 0.8, ease: 'power2.out' });
  gsap.to(displayRmse, { value: props.metrics?.return_rmse || 0, duration: 0.8, ease: 'power2.out' });
};

onMounted(() => {
  if (gridRef.value) {
    const cards = gridRef.value.querySelectorAll('.metric-card');
    gsap.fromTo(cards, 
      { opacity: 0, y: 20 },
      { opacity: 1, y: 0, duration: 0.5, stagger: 0.1, ease: 'power2.out' }
    );
  }
  animateCounters();
});

watch(() => props.metrics, () => {
  displayMape.value = 0;
  displayR2.value = 0;
  displayAcc.value = 0;
  displayRmse.value = 0;
  animateCounters();
}, { deep: true });
</script>
