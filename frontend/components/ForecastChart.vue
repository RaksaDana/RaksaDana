<template>
  <div class="glass-card rounded-2xl p-6 h-[400px] flex flex-col">
    <div class="mb-4">
      <h3 class="text-[16px] font-semibold text-light-text dark:text-dark-text">Proyeksi Harga 30 Hari</h3>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="flex-1 w-full flex flex-col justify-end gap-2 pb-6">
      <SkeletonBlock width="100%" height="280px" borderRadius="8px" />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex-1 w-full flex flex-col justify-center gap-4">
      <div class="bg-danger/10 border-l-[3px] border-danger rounded-xl p-6 flex items-start gap-3">
        <ExclamationTriangleIcon class="w-6 h-6 text-danger shrink-0 mt-0.5" />
        <div class="flex flex-col gap-2">
          <span class="text-[16px] text-danger font-medium">{{ typeof error === 'string' ? error : 'Gagal memuat chart proyeksi harga.' }}</span>
          <button @click="$emit('retry')" class="text-[14px] font-semibold text-danger underline w-fit hover:opacity-80">Coba Lagi</button>
        </div>
      </div>
    </div>
    
    <!-- Ready State -->
    <div v-else-if="forecastData && forecastData.length > 0" class="flex-1 w-full relative">
      <div class="h-[280px] w-full">
        <ClientOnly>
          <apexchart 
            type="area" 
            height="280" 
            :options="chartOptions" 
            :series="series" 
          />
        </ClientOnly>
      </div>

      <div class="mt-4 text-center">
        <p class="text-[11px] text-light-muted dark:text-dark-muted italic">
          Data model per 20 Januari 2026. Proyeksi dihitung mulai tanggal tersebut.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useColorMode } from '@vueuse/core';
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline';
import SkeletonBlock from './SkeletonBlock.vue';

const colorMode = useColorMode();

const props = defineProps({
  forecastData: {
    type: Array,
    default: () => []
  },
  baseClose: {
    type: Number,
    default: 0
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

const series = computed(() => {
  if (!props.forecastData || props.forecastData.length === 0) return [];
  return [{
    name: 'Prediksi Harga',
    data: props.forecastData.map(d => ({
      x: new Date(d.date).getTime(),
      y: d.predicted_close
    }))
  }];
});

const chartOptions = computed(() => {
  const isDark = colorMode.value === 'dark';
  
  return {
    chart: {
      type: 'area',
      fontFamily: 'Inter, sans-serif',
      background: 'transparent',
      toolbar: { show: false },
      animations: { 
        enabled: true,
        easing: 'easeinout',
        speed: 800
      }
    },
    colors: ['#3B82F6'],
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: isDark ? 0.3 : 0.2,
        opacityTo: 0.0,
        stops: [0, 100]
      }
    },
    dataLabels: { enabled: false },
    stroke: {
      curve: 'smooth',
      width: 2
    },
    xaxis: {
      type: 'datetime',
      labels: {
        style: { colors: isDark ? '#6B7A99' : '#4A5568' },
        datetimeUTC: false,
        format: 'dd MMM'
      },
      axisBorder: { show: false },
      axisTicks: { show: false },
      tooltip: { enabled: false }
    },
    yaxis: {
      labels: {
        style: { colors: isDark ? '#6B7A99' : '#4A5568' },
        formatter: (val) => {
          if (val >= 1000) return 'Rp ' + (val / 1000).toFixed(1).replace('.', ',') + 'K';
          return 'Rp ' + val;
        }
      }
    },
    grid: {
      borderColor: isDark ? '#1E2D42' : '#E2E8F4',
      strokeDashArray: 4,
      xaxis: { lines: { show: true } },
      yaxis: { lines: { show: true } }
    },
    theme: { mode: isDark ? 'dark' : 'light' },
    tooltip: {
      theme: isDark ? 'dark' : 'light',
      cssClass: 'glass-tooltip',
      y: {
        formatter: (val) => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(val)
      }
    },
    annotations: {
      yaxis: props.baseClose > 0 ? [{
        y: props.baseClose,
        borderColor: '#F59E0B',
        strokeDashArray: 5,
        label: {
          borderColor: '#F59E0B',
          style: {
            color: '#fff',
            background: '#F59E0B',
          },
          text: 'Harga Saat Ini'
        }
      }] : []
    }
  };
});
</script>

<style>
.glass-tooltip {
  background: rgba(255,255,255,0.8) !important;
  backdrop-filter: blur(10px) !important;
  border: 1px solid rgba(0,0,0,0.05) !important;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}
.dark .glass-tooltip {
  background: rgba(15, 25, 35, 0.8) !important;
  border: 1px solid rgba(255,255,255,0.05) !important;
}
</style>
