<script setup lang="ts">
import type { NavigationMenuItem } from "@nuxt/ui";

const route = useRoute();

const navigationItems = computed<NavigationMenuItem[]>(() => [
  {
    label: "Курсы",
    icon: "i-heroicons-academic-cap",
    to: "/courses",
    active: route.path.startsWith("/courses"),
  },
  {
    label: "Личный кабинет",
    icon: "i-heroicons-user-circle",
    to: "/dashboard",
    active: route.path.startsWith("/dashboard"),
  },
]);
</script>

<template>
  <div>
    <h3 class="text-sm font-semibold text-muted uppercase tracking-wider mb-3">
      Навигация
    </h3>
    <UNavigationMenu
      :items="navigationItems"
      orientation="vertical"
      class="-mx-2.5"
      :ui="{
        list: 'space-y-2',
        link: 'text-lg justify-center py-3',
        linkLeadingIcon: 'size-6',
      }"
      variant="pill"
    />
  </div>
</template>
