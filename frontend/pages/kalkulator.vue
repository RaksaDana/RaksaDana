<template>
  <div class="space-y-6">
    <div class="flex items-center gap-3 mb-6">
      <h1 class="text-[24px] font-bold text-light-text dark:text-dark-text opacity-0" ref="titleRef">Kalkulator</h1>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6" ref="contentRef">
      <!-- Calculator Form -->
      <div class="glass-card rounded-2xl p-6 stagger-item opacity-0">
        <div class="flex items-center gap-3 mb-6">
          <div class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
            <CalculatorIcon class="h-5 w-5 text-primary" />
          </div>
          <h2 class="text-[18px] font-bold text-light-text dark:text-dark-text">Simulasi Investasi</h2>
        </div>

        <form @submit.prevent="submitForm" class="space-y-6">
          <!-- Ticker Select -->
          <div class="relative">
            <label class="block text-[12px] font-medium text-light-muted dark:text-dark-muted mb-2">Pilih Saham</label>
            <div v-if="tickersLoading" class="skeleton-shimmer h-12 w-full rounded-xl"></div>
            <select v-else v-model="form.ticker" required class="w-full h-12 px-4 rounded-xl bg-light-bg dark:bg-dark-bg border border-light-border dark:border-dark-border text-light-text dark:text-dark-text focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all appearance-none cursor-pointer">
              <option value="" disabled>Pilih ticker...</option>
              <option v-for="t in tickers" :key="t" :value="t">{{ t }}</option>
            </select>
            <ChevronDownIcon v-if="!tickersLoading" class="h-5 w-5 absolute right-4 top-[38px] text-light-muted dark:text-dark-muted pointer-events-none" />
          </div>

          <!-- Input Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- Buy Price -->
            <div class="relative group">
              <input type="number" id="buy_price" v-model="form.buy_price" required min="1" step="1"
                class="peer w-full h-14 px-4 pt-4 rounded-xl bg-light-bg dark:bg-dark-bg border border-light-border dark:border-dark-border text-light-text dark:text-dark-text focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
                placeholder=" "
              />
              <label for="buy_price" class="absolute left-4 top-4 text-[14px] text-light-muted dark:text-dark-muted transition-all peer-focus:-translate-y-3 peer-focus:text-[11px] peer-focus:text-primary peer-[:not(:placeholder-shown)]:-translate-y-3 peer-[:not(:placeholder-shown)]:text-[11px]">Harga Beli (Rp)</label>
            </div>

            <!-- Lots -->
            <div class="relative group">
              <input type="number" id="lots" v-model="form.lots" required min="1" step="1"
                class="peer w-full h-14 px-4 pt-4 rounded-xl bg-light-bg dark:bg-dark-bg border border-light-border dark:border-dark-border text-light-text dark:text-dark-text focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
                placeholder=" "
              />
              <label for="lots" class="absolute left-4 top-4 text-[14px] text-light-muted dark:text-dark-muted transition-all peer-focus:-translate-y-3 peer-focus:text-[11px] peer-focus:text-primary peer-[:not(:placeholder-shown)]:-translate-y-3 peer-[:not(:placeholder-shown)]:text-[11px]">Jumlah Lot</label>
            </div>
          </div>

          <div class="h-px w-full bg-light-border dark:bg-dark-border"></div>

          <!-- Target Mode Toggle -->
          <div class="flex items-center justify-between bg-light-bg dark:bg-dark-bg p-4 rounded-xl border border-light-border dark:border-dark-border">
            <div>
              <p class="text-[14px] font-medium text-light-text dark:text-dark-text">Gunakan Prediksi AI</p>
              <p class="text-[11px] text-light-muted dark:text-dark-muted">Biarkan model menentukan harga jual</p>
            </div>
            <button 
              type="button" 
              @click="usePrediction = !usePrediction"
              :class="['relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-light-surface dark:focus:ring-offset-dark-surface', usePrediction ? 'bg-primary' : 'bg-light-muted dark:bg-dark-border']"
            >
              <span 
                :class="['inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-300', usePrediction ? 'translate-x-6' : 'translate-x-1']"
              />
            </button>
          </div>

          <!-- Dynamic Input Area -->
          <div class="overflow-hidden transition-all duration-300" :style="{ maxHeight: usePrediction ? '120px' : '80px', opacity: 1 }">
            <div v-if="usePrediction" class="space-y-6 pt-2">
              <div>
                <div class="flex justify-between items-center mb-4">
                  <label class="text-[12px] font-medium text-light-muted dark:text-dark-muted">Durasi Prediksi</label>
                  <span class="text-[14px] font-bold text-primary">{{ form.forecast_days }} Hari</span>
                </div>
                <input 
                  type="range" 
                  v-model="form.forecast_days" 
                  min="1" max="60" 
                  class="w-full h-2 bg-light-border dark:bg-dark-border rounded-lg appearance-none cursor-pointer accent-primary"
                />
                <div class="flex justify-between text-[11px] text-light-muted dark:text-dark-muted mt-2">
                  <span>1 Hari</span>
                  <span>60 Hari</span>
                </div>
              </div>
            </div>
            
            <div v-else class="pt-2">
              <div class="relative group">
                <input type="number" id="sell_price" v-model="form.sell_price" required min="1" step="1"
                  class="peer w-full h-14 px-4 pt-4 rounded-xl bg-light-bg dark:bg-dark-bg border border-light-border dark:border-dark-border text-light-text dark:text-dark-text focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
                  placeholder=" "
                />
                <label for="sell_price" class="absolute left-4 top-4 text-[14px] text-light-muted dark:text-dark-muted transition-all peer-focus:-translate-y-3 peer-focus:text-[11px] peer-focus:text-primary peer-[:not(:placeholder-shown)]:-translate-y-3 peer-[:not(:placeholder-shown)]:text-[11px]">Harga Jual Target (Rp)</label>
              </div>
            </div>
          </div>

          <button 
            type="submit" 
            :disabled="calculating"
            class="w-full py-4 px-6 rounded-xl text-white font-semibold text-[15px] shadow-lg shadow-primary/25 hover:shadow-primary/40 hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed disabled:hover:translate-y-0 relative overflow-hidden"
            :class="calculating ? 'bg-primary' : 'bg-gradient-to-r from-primary to-purple'"
          >
            <div v-if="calculating" class="absolute inset-0 skeleton-shimmer opacity-30"></div>
            <span class="relative flex items-center justify-center gap-2">
              <div v-if="calculating" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              {{ calculating ? 'Menghitung...' : 'Hitung Simulasi' }}
            </span>
          </button>
        </form>
      </div>

      <!-- Result Card -->
      <div class="stagger-item opacity-0">
        <ProfitLossResult 
          :result="resultData" 
          :loading="calculating" 
          :error="calcError" 
          :narrationResult="narrationResult"
          :narrationLoading="narrationLoading"
          :narrationError="narrationError"
          @retry="submitForm"
          @request-narration="fetchNarration"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { CalculatorIcon, ChevronDownIcon } from '@heroicons/vue/24/outline';
import { useApi } from '~/composables/useApi';
import ProfitLossResult from '~/components/ProfitLossResult.vue';
import gsap from 'gsap';

const { getTickers, calculateProfitLoss, calculateProfitLossWithNarration } = useApi();

const calcEndpoint = calculateProfitLoss();
const narrateEndpoint = calculateProfitLossWithNarration();

const titleRef = ref(null);
const contentRef = ref(null);

const usePrediction = ref(true);

const form = ref({
  ticker: '',
  buy_price: null,
  lots: null,
  sell_price: null,
  forecast_days: 30
});

const resultData = ref(null);
const calculating = ref(false);
const calcError = ref('');

const narrationResult = ref('');
const narrationLoading = ref(false);
const narrationError = ref(false);

const tickers = ref([]);
const tickersLoading = ref(true);

onMounted(async () => {
  gsap.set(titleRef.value, { y: 20 });
  
  try {
     const tEndpoint = getTickers();
     await tEndpoint.fetch();
     tickers.value = tEndpoint.data.value;
     if (tickers.value && tickers.value.length > 0) {
        form.value.ticker = tickers.value[0];
     }
  } finally {
     tickersLoading.value = false;
  }
  
  gsap.to(titleRef.value, { opacity: 1, y: 0, duration: 0.5, ease: 'power2.out', delay: 0.1 });
  if (contentRef.value) {
    const items = contentRef.value.querySelectorAll('.stagger-item');
    gsap.fromTo(items, 
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 0.5, stagger: 0.1, ease: 'power2.out', delay: 0.2 }
    );
  }
});

watch(usePrediction, (newVal) => {
  if (newVal) {
    form.value.sell_price = null;
  } else {
    form.value.forecast_days = 30;
  }
});

const getPayload = () => {
  const payload = {
    ticker: form.value.ticker,
    buy_price: parseFloat(form.value.buy_price),
    lots: parseInt(form.value.lots)
  };
  
  if (usePrediction.value) {
    payload.forecast_days = parseInt(form.value.forecast_days);
    payload.sell_price = null;
  } else {
    payload.sell_price = parseFloat(form.value.sell_price);
  }
  
  return payload;
};

const submitForm = async () => {
  calculating.value = true;
  calcError.value = '';
  narrationResult.value = '';
  narrationError.value = false;
  
  const payload = getPayload();
  
  calcEndpoint.fetch(payload).then(() => {
    resultData.value = calcEndpoint.data.value;
    calcError.value = calcEndpoint.error.value;
    calculating.value = false;
  });
};

const fetchNarration = async () => {
  narrationLoading.value = true;
  narrationError.value = false;
  
  const payload = getPayload();
  
  narrateEndpoint.fetch(payload).then(() => {
    if (narrateEndpoint.data.value?.narration) {
      narrationResult.value = narrateEndpoint.data.value.narration;
    } else {
      narrationError.value = true;
    }
    narrationLoading.value = false;
  });
};
</script>

<style scoped>
/* Custom range slider styling */
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #3B82F6;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
  transition: transform 0.1s;
}

input[type=range]::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}
</style>
