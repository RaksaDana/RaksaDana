<template>
  <div class="glass-card rounded-2xl p-6">
    <div class="mb-4">
      <h3 class="text-[16px] font-semibold text-light-text dark:text-dark-text">Proyeksi Harga 30 Hari</h3>
    </div>
    
    <div class="h-[300px] w-full">
      <ClientOnly>
        <apexchart 
          type="area" 
          height="300" 
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
</template>

<script setup>
import { computed } from 'vue';
import { useColorMode } from '@vueuse/core';

const colorMode = useColorMode();

const props = defineProps({
  forecastData: {
    type: Array,
    required: true
  },
  baseClose: {
    type: Number,
    required: true
  }
});

const series = computed(() => [{
  name: 'Prediksi Harga',
  data: props.forecastData.map(d => ({
    x: new Date(d.date).getTime(),
    y: d.predicted_close
  }))
}]);

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
      yaxis: [{
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
      }]
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
