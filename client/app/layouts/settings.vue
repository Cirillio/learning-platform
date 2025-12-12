<script setup lang="ts">
// Set title template for settings pages
useHead({
  titleTemplate: "%s | Настройки",
});
</script>

<template>
  <div class="flex flex-col bg-default min-h-dvh">
    <Header />

    <LayoutContainer class="flex flex-col flex-1 gap-4 py-6">
      <h1 class="text-3xl px-4 font-extrabold">Настройки</h1>

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

    <Footer class="mt-auto" />
  </div>
</template>
