<template>
  <Header />

  <UMain>
    <LayoutContainer class="py-2 h-full">
      <UCard
        class=""
        :ui="{
          body: '!p-0',
        }"
      >
        <template #header>
          <h1 class="text-2xl font-bold">Настройки</h1>
        </template>

        <div class="w-full min-w-0 flex">
          <div
            class="flex gap-1 flex-col bg-muted/50 p-4 max-w-[200px] w-full relative"
          >
            <UButton
              v-for="btn in settingLinks"
              :key="btn.label"
              :to="btn.to"
              :label="btn.label"
              :variant="btn.variant"
              :color="btn.color"
              size="lg"
              class="justify-start font-semibold w-full"
            />
            <div
              class="absolute h-full w-px bg-primary right-0 top-0 bottom-0"
            ></div>
          </div>

          <div class="p-4 bg-primary/10 w-full">
            <slot />
          </div>
        </div>
      </UCard>
    </LayoutContainer>
  </UMain>

  <Footer />
</template>
<script lang="ts" setup>
import type { ButtonProps } from "@nuxt/ui/runtime/components/Button.vue.js";

const settingLinks = ref<ButtonProps[]>([
  {
    to: "/settings",
    label: "Общие",
    variant: "soft",
    color: "neutral",
  },
  {
    to: "/settings/edit-profile",
    label: "Профиль",
    variant: "soft",
    color: "neutral",
  },
]);
</script>
