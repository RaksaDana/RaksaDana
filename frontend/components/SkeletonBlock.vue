<template>
  <div class="skeleton-block" :style="{ width, height, borderRadius }"></div>
</template>

<script setup>
defineProps({
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '16px'
  },
  borderRadius: {
    type: String,
    default: '4px'
  }
});
</script>

<style scoped>
.skeleton-block {
  background: #E2E8F0;
  position: relative;
  overflow: hidden;
}

.skeleton-block::after {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  transform: translateX(-100%);
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0,
    rgba(255, 255, 255, 0) 20%,
    #CBD5E1 50%,
    rgba(255, 255, 255, 0) 80%,
    rgba(255, 255, 255, 0) 100%
  );
  animation: shimmer 1.5s infinite;
}

.dark .skeleton-block {
  background: #1E293B;
}

.dark .skeleton-block::after {
  background: linear-gradient(
    90deg,
    rgba(0, 0, 0, 0) 0,
    rgba(0, 0, 0, 0) 20%,
    #334155 50%,
    rgba(0, 0, 0, 0) 80%,
    rgba(0, 0, 0, 0) 100%
  );
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}
</style>
