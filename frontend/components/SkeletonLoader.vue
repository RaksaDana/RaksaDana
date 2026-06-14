<template>
  <div :class="['skeleton-shimmer rounded-lg', customClass]"></div>
</template>

<script setup>
defineProps({
  customClass: {
    type: String,
    default: 'h-full w-full'
  }
});
</script>
