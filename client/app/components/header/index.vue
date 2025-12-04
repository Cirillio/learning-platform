<script setup lang="ts">
const authStore = useAuthStore();
const { isAuthenticated, user } = storeToRefs(authStore);

const isMobileMenuOpen = ref(false);

// Блокировка прокрутки при открытом мобильном меню
const unwatchMobileMenu = watch(isMobileMenuOpen, (newVal) => {
  if (newVal) {
    document.body.classList.add("!overflow-hidden");
  } else {
    document.body.classList.remove("!overflow-hidden");
  }
});

const headerRef = ref<HTMLElement | null>(null);
useElementHeight(headerRef, "--header-el-height");

// Очистка watch при размонтировании компонента
onUnmounted(() => {
  unwatchMobileMenu();
});
</script>

<template>
  <header
    ref="headerRef"
    class="sticky top-0 left-0 right-0 z-80 bg-default/90 backdrop-blur-sm border-b border-muted"
  >
    <LayoutContainer class="py-2">
      <div class="flex items-center justify-between">
        <!-- Logo -->
        <HeaderLeading />

        <!-- Desktop Actions -->
        <div class="hidden md:flex items-center gap-2">
          <HeaderDesktopAuth v-if="!isAuthenticated" />
          <div v-else class="flex items-center gap-2">
            <HeaderDesktopUserActions :user="user" />
            <USeparator orientation="vertical" color="neutral" class="h-6" />
            <HeaderDesktopActions />
          </div>
        </div>

        <!-- Mobile Menu -->
        <HeaderMobileMenu>
          <!-- Mobile Menu Toggle -->
          <HeaderMobileToggleButton class="md:hidden" />
        </HeaderMobileMenu>
      </div>
    </LayoutContainer>
  </header>

  <HeaderDesktopNavigation class="max-md:hidden" />
</template>
