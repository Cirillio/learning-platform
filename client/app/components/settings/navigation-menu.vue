<script lang="ts" setup>
import type { NavigationMenuItem } from "@nuxt/ui";

const sidebarItems = ref<NavigationMenuItem[]>([
  {
    label: "Общие",
    to: "/settings",
    icon: "i-lucide-settings-2",
  },
  { label: "Профиль", to: "/settings/account", icon: "i-lucide-user" },
  {
    label: "Конфиденциальность",
    to: "/settings/privacy",
    icon: "i-lucide-lock",
  },
  {
    label: "Уведомления",
    to: "/settings/notifications",
    icon: "i-lucide-bell",
  },
  { label: "Оплата", to: "/settings/billing", icon: "i-lucide-credit-card" },
]);
</script>
<template>
  <UNavigationMenu
    orientation="vertical"
    :items="sidebarItems"
    class="flex h-full flex-col bg-muted/50 border-r border-default p-3 max-w-[280px] w-full relative"
    color="secondary"
    variant="pill"
    :ui="{
      list: 'space-y-2',
      link: 'font-medium max-sm:w-fit text-lg text-muted hover:text-highlighted data-[active=true]:text-highlighted data-[active=true]:font-bold',
      linkLeadingIcon:
        'text-muted group-hover:text-highlighted group-data-[active=true]:text-highlighted',
      linkLabel: 'max-sm:hidden',
    }"
  />
</template>
