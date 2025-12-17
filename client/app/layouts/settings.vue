<script setup lang="ts">
// Set title template for settings pages
useHead({
  titleTemplate: "%s | Настройки",
});
</script>

<template>
  <div class="flex flex-col bg-default min-h-dvh">
    <LayoutContainer class="flex flex-col flex-1 gap-4 py-6">
      <div>
        <UButton
          label="Назад"
          icon="heroicons:chevron-left"
          variant="link"
          color="neutral"
          @click="navigateTo('/')"
        />
        <h1 class="text-3xl px-4 font-extrabold">Настройки</h1>
      </div>

      <UCard
        class="flex-1 flex"
        :ui="{
          body: '!p-0  flex-1',
        }"
      >
        <div class="w-full flex h-full">
          <SettingsNavigationMenu />

          <div class="p-3 w-full">
            <slot />
          </div>
        </div>
      </UCard>
    </LayoutContainer>
  </div>
</template>
