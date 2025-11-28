<script lang="ts" setup>
import type { NavigationMenuItem } from "@nuxt/ui";

const route = useRoute();

const infoActions = [
  {
    label: "Цены",
    to: "/pricing",
  },
  {
    label: "Почему выбирают нас",
    to: "/why-us",
  },
];

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
  <LayoutContainer class="flex justify-between border-b border-muted py-1">
    <div class="flex items-center gap-4">
      <NuxtLink v-for="item in infoActions" :key="item.label" :to="item.to">
        <UButton
          :label="item.label"
          variant="link"
          color="neutral"
          size="md"
          class="cursor-pointer px-0 hover:text-default"
        />
      </NuxtLink>
    </div>

    <div class="flex items-center gap-4">
      <NuxtLink v-for="item in mainActions" :key="item.label" :to="item.to">
        <UButton
          :label="item.label"
          color="neutral"
          variant="link"
          size="md"
          class="cursor-pointer px-0 hover:text-default"
        />
      </NuxtLink>
    </div>
  </LayoutContainer>
</template>
