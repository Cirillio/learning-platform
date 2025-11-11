<script setup lang="ts">
// Компоненты импортируются автоматически через auto-imports
</script>

<template>
  <UHeader
    mode="slideover"
    :toggle="{
      color: 'primary',
      variant: 'ghost',
      class: 'rounded-full lg:hidden',
    }"
    :ui="{
      root: 'bg-background/95 backdrop-blur relative border-0 border-b border-primary/25',
    }"
  >
    <template #title>
      <AppLogo />
    </template>

    <!-- Desktop navigation -->
    <div class="hidden lg:block">
      <HeaderNavigationMenuDesktop />
    </div>

    <template #right>
      <!-- Desktop auth actions -->
      <div class="hidden lg:block">
        <HeaderAuthActionsDesktop />
      </div>

      <!-- Mobile menu toggle is automatically added by UHeader -->
    </template>

    <!-- Mobile menu content -->
    <template #body>
      <div class="space-y-6">
        <HeaderNavigationMenuMobile />
        <HeaderAuthActionsMobile />
        <HeaderThemeToggle />
      </div>
    </template>
  </UHeader>
</template>
