<template>
  <div class="space-y-6 overflow-hidden">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4" ref="headerRef">
      <h1 class="text-[24px] font-bold text-light-text dark:text-dark-text opacity-0" ref="titleRef">Dashboard</h1>
      
      <!-- Ticker Selector -->
      <div v-if="tickers && tickers.length > 0" class="flex p-1 bg-light-surface dark:bg-dark-surface rounded-full border border-light-border dark:border-dark-border w-fit shadow-sm">
        <button 
          v-for="t in tickers" 
          :key="t"
          @click="selectTicker(t)"
          :class="[
            'px-6 py-2 rounded-full text-[14px] font-medium transition-all duration-300',
            activeTicker === t 
              ? 'bg-gradient-to-r from-primary to-purple text-white shadow-md' 
              : 'text-light-muted dark:text-dark-muted hover:bg-light-elevated dark:hover:bg-dark-elevated bg-transparent'
          ]"
        >
          {{ t.split('.')[0] }}
        </button>
      </div>
      <div v-else-if="tickersLoading" class="w-64 h-10 rounded-full bg-light-surface dark:bg-dark-surface animate-pulse"></div>
    </div>

    <!-- Error State Global -->
    <div v-if="tickersError" class="bg-danger/10 border border-danger/20 rounded-xl p-4 text-danger text-[14px]">
      {{ tickersError }}
      <button @click="fetchTickers" class="ml-4 underline font-medium">Coba Lagi</button>
    </div>

    <!-- Main Content Grid -->
    <div ref="contentRef" class="grid grid-cols-1 lg:grid-cols-3 gap-6 relative">
      <!-- Loading Overlay -->
      <div v-if="isSwitching" class="absolute inset-0 z-10 flex items-center justify-center bg-light-bg/50 dark:bg-dark-bg/50 backdrop-blur-sm rounded-2xl transition-opacity duration-300">
         <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>
      
      <!-- Left Column (Signal & Metrics & Forecast) -->
      <div class="lg:col-span-2 space-y-6 stagger-item opacity-0">
        <!-- Signal Hero Card -->
        <div v-if="predictionLoading && !isSwitching">
          <SkeletonLoader customClass="h-48 w-full" />
        </div>
        <SignalCard 
          v-else-if="predictionData" 
          :prediction="predictionData" 
        />
        <div v-else-if="predictionError && !isSwitching" class="glass-card h-48 rounded-2xl flex items-center justify-center">
          <span class="text-danger">{{ predictionError }}</span>
        </div>

        <!-- Metrics Grid -->
        <div v-if="metricsLoading && !isSwitching">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <SkeletonLoader v-for="i in 4" :key="i" customClass="h-[120px] w-full" />
          </div>
        </div>
        <MetricsGrid 
          v-else-if="metricsData" 
          :metrics="metricsData" 
        />

        <!-- Forecast Chart -->
        <div v-if="forecastLoading && !isSwitching">
          <SkeletonLoader customClass="h-[380px] w-full" />
        </div>
        <ForecastChart 
          v-else-if="forecastData && predictionData" 
          :forecastData="forecastData"
          :baseClose="predictionData.base_close"
        />
      </div>

      <!-- Right Column (Narration) -->
      <div class="lg:col-span-1 stagger-item opacity-0">
        <NarrationCard 
          :loading="predictionLoading && !isSwitching"
          :error="predictionError"
          :narration="predictionData?.narration"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useApi } from '~/composables/useApi';
import SignalCard from '~/components/SignalCard.vue';
import MetricsGrid from '~/components/MetricsGrid.vue';
import ForecastChart from '~/components/ForecastChart.vue';
import NarrationCard from '~/components/NarrationCard.vue';
import gsap from 'gsap';

const { getTickers, getPrediction, getForecast, getMetrics } = useApi();

const { data: tickers, loading: tickersLoading, error: tickersError, fetch: fetchTickers } = getTickers();

const activeTicker = ref('');
const isSwitching = ref(false);

const titleRef = ref(null);
const contentRef = ref(null);

// Endpoints
let predEndpoint, forecastEndpoint, metricsEndpoint;

// Refs
const predictionData = ref(null);
const predictionLoading = ref(false);
const predictionError = ref(null);

const forecastData = ref(null);
const forecastLoading = ref(false);

const metricsData = ref(null);
const metricsLoading = ref(false);

const animateEntrance = () => {
  gsap.to(titleRef.value, { opacity: 1, y: 0, duration: 0.5, ease: 'power2.out', delay: 0.1 });
  
  if (contentRef.value) {
    const items = contentRef.value.querySelectorAll('.stagger-item');
    gsap.fromTo(items, 
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 0.5, stagger: 0.1, ease: 'power2.out', delay: 0.2 }
    );
  }
};

onMounted(async () => {
  gsap.set(titleRef.value, { y: 20 });
  
  const res = await fetchTickers();
  if (res && res.length > 0) {
    activeTicker.value = res[0];
    await loadTickerData(res[0]);
  }
  
  nextTick(() => {
    animateEntrance();
  });
});

const selectTicker = async (ticker) => {
  if (activeTicker.value === ticker) return;
  
  // GSAP Fade out content
  const items = contentRef.value.querySelectorAll('.stagger-item');
  await gsap.to(items, { opacity: 0, y: 10, duration: 0.15, ease: 'power2.in' });
  
  activeTicker.value = ticker;
  isSwitching.value = true;
  await loadTickerData(ticker);
  isSwitching.value = false;
  
  // GSAP Fade in content
  gsap.fromTo(items, 
    { opacity: 0, y: 20 },
    { opacity: 1, y: 0, duration: 0.3, stagger: 0.1, ease: 'power2.out' }
  );
};

const loadTickerData = async (ticker) => {
  predEndpoint = getPrediction(ticker);
  forecastEndpoint = getForecast(ticker, 30);
  metricsEndpoint = getMetrics(ticker);

  predictionLoading.value = true;
  forecastLoading.value = true;
  metricsLoading.value = true;

  const [predRes, foreRes, metRes] = await Promise.allSettled([
    predEndpoint.fetch(),
    forecastEndpoint.fetch(),
    metricsEndpoint.fetch()
  ]);

  if (predRes.status === 'fulfilled') {
    predictionData.value = predEndpoint.data.value;
    predictionError.value = predEndpoint.error.value;
  }
  predictionLoading.value = false;

  if (foreRes.status === 'fulfilled') {
    forecastData.value = forecastEndpoint.data.value;
  }
  forecastLoading.value = false;

  if (metRes.status === 'fulfilled') {
    metricsData.value = metricsEndpoint.data.value;
  }
  metricsLoading.value = false;
};
</script>
