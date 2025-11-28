<script lang="ts" setup>
import type { NavigationMenuItem } from "@nuxt/ui";

const route = useRoute();

const mainActions = computed<NavigationMenuItem[]>(() => [
  {
    label: "Курсы",
    icon: "i-heroicons-academic-cap",
    to: route.path === "/courses" ? route.fullPath : "/courses",
    active:
      route.path === "/courses" ||
      (route.path.startsWith("/courses") &&
        !route.path.startsWith("/courses/categories")),
  },
  {
    label: "Категории",
    icon: "i-heroicons-user-circle",
    to: "/courses/categories",
    active: route.path.startsWith("/courses/categories"),
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
  <div class="w-full flex flex-col items-center gap-1">
    <NuxtLink
      class="w-full"
      v-for="item in mainActions"
      :key="item.label"
      :to="item.to"
    >
      <UButton
        :label="item.label"
        color="neutral"
        variant="outline"
        block
        class="cursor-pointer justify-start hover:text-default"
      />
    </NuxtLink>
  </div>
</template>
