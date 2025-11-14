<script setup lang="ts">
import type { DropdownMenuItem } from "@nuxt/ui";
const { isAuthenticated, user } = useAuthStore();

const profileItems = ref<DropdownMenuItem[]>([
  {
    label: "Профиль",
    icon: "heroicons:user-circle",
    href: "/profile",
    color: "primary",
  },
  {
    label: "Мои курсы",
    icon: "heroicons:code-bracket-square",
    href: "/settings",
    color: "info",
  },
  {
    label: "Выйти",
    icon: "heroicons:arrow-uturn-right",
    href: "/auth/logout",
    color: "error",
  },
]);
</script>

<template>
  <UHeader
    mode="slideover"
    :toggle="{
      color: 'primary',
      variant: 'ghost',
      class: 'rounded-md lg:hidden',
    }"
    :ui="{
      root: 'border-0 ring-0 backdrop-blur-md bg-muted/80',
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
        <HeaderAuthActionsDesktop v-if="!isAuthenticated" />
        <UDropdownMenu
          v-else
          :items="profileItems"
          :content="{
            align: 'center',
            side: 'bottom',
            sideOffset: 8,
          }"
          :ui="{
            content: 'w-fit rounded-sm ring-0 bg-inverted/5',
            viewport: '!overflow-visible',
          }"
        >
          <div
            class="flex cursor-pointer hover:border-secondary/50 gap-2 border rounded-full items-center px-4 py-1.5 bg-muted transition-all duration-200 ease-in-out"
            :class="[
              $route.path === '/dashboard' ? 'border-secondary' : 'border-transparent',
            ]"
          >
            <span class="font-semibold text-base">
              {{ user?.first_name }} {{ user?.last_name }}
            </span>
            <UIcon class="text-secondary size-5" name="heroicons-user" />
          </div>
        </UDropdownMenu>
      </div>

      <!-- Mobile menu toggle is automatically added by UHeader -->
    </template>

    <!-- Mobile menu content -->
    <template #body>
      <div class="space-y-6">
        <HeaderNavigationMenuMobile />
        <HeaderAuthActionsMobile v-if="!isAuthenticated" />
        <HeaderThemeToggle />
      </div>
    </template>
  </UHeader>
</template>
