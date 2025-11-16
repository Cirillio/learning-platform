<script setup lang="ts">
import { watch } from "vue";

const authStore = useAuthStore();
const { isAuthenticated, user } = storeToRefs(authStore);

const isMobileMenuOpen = ref(false);

// Блокировка прокрутки при открытом мобильном меню
watch(isMobileMenuOpen, (newVal) => {
  if (newVal) {
    document.body.classList.add("!overflow-hidden");
  } else {
    document.body.classList.remove("!overflow-hidden");
  }
});
</script>

<template>
  <header
    class="sticky top-0 z-50 bg-background/80 backdrop-blur-sm border-b border-muted"
  >
    <UContainer class="py-2">
      <div class="flex items-center justify-between">
        <!-- Logo -->
        <AppLogo />

        <!-- Desktop Actions -->
        <HeaderDesktop />

        <!-- Mobile Menu Toggle -->
        <div class="md:hidden">
          <HeaderMobileToggle @toggle="isMobileMenuOpen = !isMobileMenuOpen" />
        </div>
      </div>

      <!-- Mobile Menu -->
      <HeaderMobileMenu :is-visible="isMobileMenuOpen" :is-authenticated="isAuthenticated" />
    </UContainer>
  </header>
</template>
