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
      root: 'border-t-px! border-muted py-2 bg-muted/75 dark:bg-muted/25 ',
      container:
        '!items-stretch max-lg:flex max-lg:flex-col-reverse max-w-full main-container',
      left: 'max-lg:items-center',
      right:
        'flex flex-col !justify-between items-end min-h-full max-lg:items-center gap-4',
    }"
  >
    <template #left>
      <div class="flex flex-col gap-12 lg:gap-24 justify-between">
        <NuxtLink
          to="/"
          class="flex *:text-default hover:*:text-primary gap-2 items-center max-sm:flex-col max-sm:text-center"
        >
          <AppLogo class="size-8" />
          <span
            class="text-2xl font-semibold transition-all duration-150 ease-in-out"
            >Образовательный портал</span
          >
        </NuxtLink>

        <div class="flex flex-col max-lg:gap-4 gap-2 max-lg:items-center">
          <div class="flex gap-2 max-lg:gap-4">
            <UButton
              icon="i-simple-icons-github"
              color="neutral"
              variant="ghost"
              to="https://github.com"
              target="_blank"
              aria-label="GitHub"
            />
            <UColorModeButton />
          </div>
          <UBadge
            label="Найдите то, что вас вдохновит"
            variant="subtle"
            size="xl"
            class="justify-center"
          />
        </div>
      </div>
    </template>

    <USeparator class="lg:hidden w-1/5 my-4" />

    <template #right>
      <div class="flex gap-1 flex-col max-lg:items-center items-end">
        <UButton
          v-for="link in footerLinks"
          :key="link.label"
          :to="link.to"
          variant="link"
          color="neutral"
          class="hover:text-primary transition-all justify-end duration-150 w-fit max-lg:text-lg"
        >
          {{ link.label }}
        </UButton>
      </div>

      <p
        class="text-lg font-semibold text-muted self-center lg:self-end max-sm:text-center"
      >
        © {{ new Date().getFullYear() }} Учебный портал. Все права защищены.
      </p>
    </template>
  </UFooter>
</template>
