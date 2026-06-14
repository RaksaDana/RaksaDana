<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" ref="gridRef">
    <!-- MAPE -->
    <div class="metric-card glass-card rounded-xl p-4 hover:-translate-y-1 hover:shadow-[0_0_15px_rgba(59,130,246,0.15)] transition-all duration-200">
      <div class="flex flex-col gap-2">
        <div class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
          <ChartBarIcon class="h-5 w-5 text-primary" />
        </div>
        <p class="text-[11px] uppercase text-light-muted dark:text-dark-muted font-semibold tracking-wider mt-2">MAPE</p>
        <h3 class="text-[28px] font-bold text-light-text dark:text-dark-text">{{ displayMape.toFixed(2).replace('.', ',') }}<span class="text-[16px] text-light-muted dark:text-dark-muted" v-if="metrics?.mape !== undefined">%</span></h3>
        <p class="text-[12px] text-light-muted dark:text-dark-muted">Rata-rata error prediksi</p>
      </div>
    </div>
    
    <!-- R2 -->
    <div class="metric-card glass-card rounded-xl p-4 hover:-translate-y-1 hover:shadow-[0_0_15px_rgba(16,185,129,0.15)] transition-all duration-200">
      <div class="flex flex-col gap-2">
        <div class="w-10 h-10 rounded-full bg-success/10 flex items-center justify-center">
          <CheckBadgeIcon class="h-5 w-5 text-success" />
        </div>
        <p class="text-[11px] uppercase text-light-muted dark:text-dark-muted font-semibold tracking-wider mt-2">R² Score</p>
        <h3 class="text-[28px] font-bold text-light-text dark:text-dark-text">{{ displayR2.toFixed(2).replace('.', ',') }}<span class="text-[16px] text-light-muted dark:text-dark-muted" v-if="metrics?.r2 !== undefined">%</span></h3>
        <p class="text-[12px] text-light-muted dark:text-dark-muted">Kesesuaian trend model</p>
      </div>
    </div>
    
    <!-- Akurasi Arah -->
    <div class="metric-card glass-card rounded-xl p-4 hover:-translate-y-1 hover:shadow-[0_0_15px_rgba(245,158,11,0.15)] transition-all duration-200">
      <div class="flex flex-col gap-2">
        <div class="w-10 h-10 rounded-full bg-warning/10 flex items-center justify-center">
          <ArrowTrendingUpIcon class="h-5 w-5 text-warning" />
        </div>
        <p class="text-[11px] uppercase text-light-muted dark:text-dark-muted font-semibold tracking-wider mt-2">Akurasi Arah</p>
        <h3 class="text-[28px] font-bold text-light-text dark:text-dark-text">{{ displayAcc.toFixed(2).replace('.', ',') }}<span class="text-[16px] text-light-muted dark:text-dark-muted" v-if="metrics?.direction_accuracy !== undefined">%</span></h3>
        <p class="text-[12px] text-light-muted dark:text-dark-muted">Ketepatan arah pergerakan</p>
      </div>
    </div>
    
    <!-- Return RMSE -->
    <div class="metric-card glass-card rounded-xl p-4 hover:-translate-y-1 hover:shadow-[0_0_15px_rgba(139,92,246,0.15)] transition-all duration-200">
      <div class="flex flex-col gap-2">
        <div class="w-10 h-10 rounded-full bg-purple/10 flex items-center justify-center">
          <CalculatorIcon class="h-5 w-5 text-purple" />
        </div>
        <p class="text-[11px] uppercase text-light-muted dark:text-dark-muted font-semibold tracking-wider mt-2">Return RMSE</p>
        <h3 class="text-[28px] font-bold text-light-text dark:text-dark-text">{{ displayRmse.toFixed(2).replace('.', ',') }}<span class="text-[16px] text-light-muted dark:text-dark-muted" v-if="metrics?.return_rmse !== undefined">%</span></h3>
        <p class="text-[12px] text-light-muted dark:text-dark-muted">Standar deviasi return</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { ChartBarIcon, CheckBadgeIcon, ArrowTrendingUpIcon, CalculatorIcon } from '@heroicons/vue/24/outline';
import gsap from 'gsap';

const props = defineProps({
  metrics: {
    type: Object,
    default: () => ({})
  }
});

const gridRef = ref(null);

const displayMape = ref(0);
const displayR2 = ref(0);
const displayAcc = ref(0);
const displayRmse = ref(0);

const animateCounters = () => {
  gsap.to(displayMape, { value: props.metrics?.mape || 0, duration: 0.8, ease: 'power2.out' });
  gsap.to(displayR2, { value: (props.metrics?.r2 || 0) * 100, duration: 0.8, ease: 'power2.out' });
  gsap.to(displayAcc, { value: props.metrics?.direction_accuracy || 0, duration: 0.8, ease: 'power2.out' });
  gsap.to(displayRmse, { value: (props.metrics?.return_rmse || 0) * 100, duration: 0.8, ease: 'power2.out' });
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
