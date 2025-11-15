<script setup lang="ts">
import type { NavigationMenuItem } from "@nuxt/ui";

const route = useRoute();

const navigationItems = computed<NavigationMenuItem[]>(() => [
  {
    label: "Личный кабинет",
    icon: "i-heroicons-user-circle",
    to: "/profile",
    active: route.path.startsWith("/profile"),
  },
  {
    label: "Курсы",
    icon: "i-heroicons-academic-cap",
    to: "/courses",
    active: route.path.startsWith("/courses"),
  },
  {
    label: "Мои курсы",
    icon: "i-heroicons-code-bracket-square",
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
    <div class="flex flex-col gap-2">
      <UButton
        v-for="link in navigationItems"
        :key="link.label"
        :to="link.to"
        :label="link.label"
        :leading-icon="link.icon"
        :variant="link.active ? 'solid' : 'subtle'"
        :color="link.active ? 'primary' : 'neutral'"
        class="text-lg"
      />
    </div>

    <UButton label="Выйти" color="error" class="text-lg mt-4" block />
  </div>
</template>
