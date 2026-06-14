<template>
  <div class="glass-card rounded-2xl overflow-hidden flex flex-col h-full" ref="resultCardRef">
    <div v-if="loading" class="p-6 space-y-4">
      <SkeletonLoader customClass="h-16 w-full" />
      <div class="grid grid-cols-2 gap-4">
        <SkeletonLoader v-for="i in 6" :key="i" customClass="h-20 w-full" />
      </div>
    </div>
    
    <div v-else-if="error" class="p-6 text-center text-danger text-[14px]">
      {{ error }}
    </div>
    
    <div v-else-if="result" class="flex flex-col h-full">
      <!-- Status Banner -->
      <div :class="['py-4 px-6 text-center text-[20px] font-bold text-white tracking-widest uppercase', statusClass]">
        {{ statusText }}
      </div>
      
      <div class="p-6 flex-1 flex flex-col gap-6">
        <!-- Summary Grid -->
        <div class="grid grid-cols-2 gap-x-4 gap-y-6">
          <div>
            <p class="text-[12px] text-light-muted dark:text-dark-muted mb-1">Net {{ result.status === 'PROFIT' ? 'Profit' : 'Loss' }}</p>
            <h3 :class="['text-[24px] font-bold', statusTextClass]">{{ formatCurrency(displayNetProfit) }}</h3>
          </div>
          <div>
            <p class="text-[12px] text-light-muted dark:text-dark-muted mb-1">Return</p>
            <h3 :class="['text-[24px] font-bold', statusTextClass]">{{ displayReturn.toFixed(2).replace('.', ',') }}%</h3>
          </div>
          <div>
            <p class="text-[12px] text-light-muted dark:text-dark-muted mb-1">Harga Beli</p>
            <p class="text-[16px] font-semibold text-light-text dark:text-dark-text">{{ formatCurrency(result.buy_price) }}</p>
          </div>
          <div>
            <p class="text-[12px] text-light-muted dark:text-dark-muted mb-1">Harga Jual</p>
            <p class="text-[16px] font-semibold text-light-text dark:text-dark-text">{{ formatCurrency(result.sell_price) }}</p>
          </div>
          <div>
            <p class="text-[12px] text-light-muted dark:text-dark-muted mb-1">Breakeven Price</p>
            <p class="text-[16px] font-semibold text-light-text dark:text-dark-text">{{ formatCurrency(result.breakeven_sell_price) }}</p>
          </div>
          <div>
            <p class="text-[12px] text-light-muted dark:text-dark-muted mb-1">Total Saham</p>
            <p class="text-[16px] font-semibold text-light-text dark:text-dark-text">{{ result.quantity.shares.toLocaleString('id-ID') }} lbr</p>
            <p class="text-[11px] text-light-muted dark:text-dark-muted">{{ result.quantity.lots }} lot</p>
          </div>
        </div>

        <div class="h-px w-full bg-light-border dark:bg-dark-border my-2"></div>

        <!-- Fee Breakdown -->
        <details class="group">
          <summary class="flex items-center justify-between cursor-pointer list-none text-[14px] font-medium text-light-text dark:text-dark-text focus:outline-none">
            Rincian Biaya Transaksi
            <span class="transition-transform duration-300 group-open:rotate-180">
              <svg fill="none" height="20" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="20"><path d="M6 9l6 6 6-6"></path></svg>
            </span>
          </summary>
          <div class="overflow-hidden transition-all duration-300 max-h-0 group-open:max-h-64 mt-4">
            <div class="space-y-2 text-[12px] text-light-muted dark:text-dark-muted">
              <div class="flex justify-between">
                <span>Gross Beli</span>
                <span>{{ formatCurrency(result.gross_buy_value) }}</span>
              </div>
              <div class="flex justify-between text-danger">
                <span>Biaya Beli ({{ (result.assumptions.buy_fee_rate * 100).toFixed(2) }}%)</span>
                <span>{{ formatCurrency(result.buy_fee) }}</span>
              </div>
              <div class="flex justify-between border-t border-light-border dark:border-dark-border pt-2 mt-2 font-medium text-light-text dark:text-dark-text">
                <span>Total Modal Keluar</span>
                <span>{{ formatCurrency(result.total_cost) }}</span>
              </div>
              
              <div class="flex justify-between mt-4">
                <span>Gross Jual</span>
                <span>{{ formatCurrency(result.gross_sell_value) }}</span>
              </div>
              <div class="flex justify-between text-danger">
                <span>Biaya Jual ({{ (result.assumptions.sell_fee_rate * 100).toFixed(2) }}%)</span>
                <span>{{ formatCurrency(result.sell_fee) }}</span>
              </div>
              <div class="flex justify-between border-t border-light-border dark:border-dark-border pt-2 mt-2 font-medium text-light-text dark:text-dark-text">
                <span>Net Dana Diterima</span>
                <span>{{ formatCurrency(result.net_proceeds) }}</span>
              </div>
            </div>
          </div>
        </details>
        
        <div class="h-px w-full bg-light-border dark:bg-dark-border my-2" v-if="result.narration"></div>

        <NarrationCard v-if="result.narration" :narration="result.narration" :loading="false" />
      </div>
    </div>
    
    <div v-else class="p-6 h-full flex items-center justify-center text-light-muted dark:text-dark-muted text-[14px]">
      Isi form di sebelah kiri untuk melihat hasil simulasi.
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue';
import { formatCurrency } from '~/utils/formatters';
import SkeletonLoader from './SkeletonLoader.vue';
import NarrationCard from './NarrationCard.vue';
import gsap from 'gsap';

const props = defineProps({
  result: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
});

const resultCardRef = ref(null);
const displayNetProfit = ref(0);
const displayReturn = ref(0);

const statusText = computed(() => {
  if (props.result?.status === 'PROFIT') return 'Untung';
  if (props.result?.status === 'LOSS') return 'Rugi';
  return 'Impas';
});

const statusClass = computed(() => {
  if (props.result?.status === 'PROFIT') return 'bg-gradient-to-r from-success to-emerald-400';
  if (props.result?.status === 'LOSS') return 'bg-gradient-to-r from-danger to-rose-400';
  return 'bg-gradient-to-r from-warning to-amber-400';
});

const statusTextClass = computed(() => {
  if (props.result?.status === 'PROFIT') return 'text-success';
  if (props.result?.status === 'LOSS') return 'text-danger';
  return 'text-warning';
});

const animateCounters = () => {
  if (props.result) {
    gsap.to(displayNetProfit, { value: props.result.net_profit_loss, duration: 0.8, ease: 'power2.out' });
    gsap.to(displayReturn, { value: props.result.net_return_pct * 100, duration: 0.8, ease: 'power2.out' });
  }
};

watch(() => props.result, (newVal) => {
  if (newVal) {
    displayNetProfit.value = 0;
    displayReturn.value = 0;
    
    if (resultCardRef.value) {
      gsap.fromTo(resultCardRef.value, 
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.4, ease: 'power2.out' }
      );
    }
    
    setTimeout(animateCounters, 100);
  }
});
</script>

<style scoped>
details > summary {
  list-style: none;
}
details > summary::-webkit-details-marker {
  display: none;
}
</style>
