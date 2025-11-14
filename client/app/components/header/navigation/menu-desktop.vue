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
  <div class="flex">
    <NuxtLink
      v-for="item in navigationItems"
      :key="item.label"
      :to="item.to"
      :class="{
        'text-primary border-primary': item.active,
        'hover:text-primary border-transparent': !item.active,
      }"
      class="px-3 flex border-b-2 items-center justify-center font-semibold py-1.5 transition-all duration-150"
    >
      {{ item.label }}
    </NuxtLink>
  </div>
</template>
