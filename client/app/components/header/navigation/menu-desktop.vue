<script lang="ts" setup>
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
  <div class="flex gap-1.5 bg-elevated p-1 rounded-full">
    <NuxtLink
      v-for="item in navigationItems"
      :key="item.label"
      :to="item.to"
      :class="{
        'bg-primary text-inverted': item.active,
      }"
      class="px-4 flex items-center justify-center font-semibold py-1.5 rounded-full transition-all duration-100"
    >
      {{ item.label }}
    </NuxtLink>
  </div>
</template>
