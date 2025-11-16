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
    label: "Расписание",
    icon: "i-heroicons-user-circle",
    to: "/schedule",
    active: route.path.startsWith("/schedule"),
  },
  {
    label: "Библиотека",
    icon: "i-heroicons-book-open",
    to: "/library",
    active: route.path.startsWith("/library"),
  },
]);
</script>

<template>
  <div
    class="flex hover:border-secondary/50 transition-all duration-150 bg-default p-1 gap-2 border border-muted rounded-sm"
  >
    <NuxtLink
      v-for="item in navigationItems"
      :key="item.label"
      :to="item.to"
      :class="{
        'text-inverted bg-primary': item.active,
        'hover:text-primary border-transparent hover:bg-inverted/5': !item.active,
      }"
      class="px-4 flex items-center rounded-xs justify-center font-semibold py-2.5 transition-all duration-150"
    >
      {{ item.label }}
    </NuxtLink>
  </div>
</template>
