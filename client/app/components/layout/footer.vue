<script setup lang="ts">
import type { NavigationMenuItem } from "@nuxt/ui";

const footerLinks: NavigationMenuItem[] = [
  {
    label: "О портале",
    to: "/about",
  },
  {
    label: "Помощь",
    to: "/help",
  },
  {
    label: "Обратная связь",
    to: "/feedback",
  },
];
</script>

<template>
  <UFooter
    :ui="{
      root: 'border-t border-primary/50',
    }"
  >
    <template #left>
      <div class="flex flex-col gap-3 max-lg:items-center">
        <AppLogo :label="'Учебный портал'" />
        <p class="text-sm text-muted">
          © {{ new Date().getFullYear() }} Учебный портал. Все права защищены.
        </p>
      </div>
    </template>

    <div class="flex gap-1">
      <UButton
        v-for="link in footerLinks"
        :key="link.label"
        :to="link.to"
        variant="link"
        color="neutral"
        class="hover:text-primary transition-all duration-150"
      >
        {{ link.label }}
      </UButton>
    </div>

    <template #right>
      <UButton
        icon="i-simple-icons-github"
        color="neutral"
        variant="ghost"
        to="https://github.com"
        target="_blank"
        aria-label="GitHub"
      />
    </template>
  </UFooter>
</template>
