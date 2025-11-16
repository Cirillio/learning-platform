<script setup lang="ts">
import type { DropdownMenuItem } from "@nuxt/ui";

const authStore = useAuthStore();
const { isAuthenticated } = storeToRefs(authStore);

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
    href: "/dashboard",
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
  <div class="hidden md:flex items-center gap-2">
    <!-- Desktop Navigation -->
    <HeaderNavigationMenuDesktop />
    <HeaderAuthActionsDesktop v-if="!isAuthenticated" />
    <UDropdownMenu
      v-else
      :items="profileItems"
      :content="{
        align: 'end',
        side: 'bottom',
        sideOffset: 16,
      }"
      size="xl"
      :ui="{
        content:
          'w-fit rounded-sm ring-0 bg-default border border-muted hover:border-secondary/50 transition-all duration-150',
        viewport: '!overflow-visible',
        item: 'hover:bg-inverted/5 rounded-xs',
      }"
    >
      <div
        class="flex cursor-pointer hover:border-secondary/50 gap-2 border items-center p-3.5 bg-default rounded-sm transition-all duration-200 ease-in-out"
        :class="[$route.path === '/profile' ? 'border-primary' : 'border-muted']"
      >
        <UIcon class="text-primary size-6" name="heroicons-user" />
      </div>
    </UDropdownMenu>
  </div>
</template>