<template>
  <div class="min-h-screen flex text-light-text dark:text-dark-text bg-light-bg dark:bg-dark-bg transition-colors duration-300 relative z-10">
    <!-- Desktop Sidebar -->
    <AppSidebar class="hidden lg:flex" />

    <!-- Main Content -->
    <main class="flex-1 pb-20 lg:pb-0 overflow-y-auto min-h-screen relative">
      <div class="p-4 lg:p-6 max-w-7xl mx-auto">
        <slot />
      </div>
    </main>

    <!-- Mobile Bottom Nav -->
    <AppBottomNav class="lg:hidden" />
  </div>
</template>
