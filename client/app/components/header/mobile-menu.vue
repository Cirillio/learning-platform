<script setup lang="ts">
interface Props {
  isVisible: boolean;
  isAuthenticated: boolean;
}

defineProps<Props>();
</script>

<template>
  <div v-if="isVisible" class="md:hidden mt-4 pb-4 border-t border-muted pt-4">
    <div class="space-y-6">
      <HeaderNavigationMenuMobile />
      <HeaderAuthActionsMobile v-if="!isAuthenticated" />
      <HeaderThemeToggle />
    </div>
  </div>
</template>