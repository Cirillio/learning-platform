<template>
  <LayoutHeader />

  <UMain class="space-y-4 py-16">
    <UContainer>
      <div
        class="flex gap-1 p-1 max-w-xl border border-muted rounded-sm hover:border-secondary/50 transition-all duration-150"
      >
        <UButton
          v-for="page in pages"
          :key="page.title"
          :to="page.path"
          :label="page.title"
          :color="$route.path === page.path ? 'primary' : 'neutral'"
          :variant="$route.path === page.path ? 'solid' : 'ghost'"
          class="w-full flex-1 justify-center text-lg"
          :class="[$route.path === page.path ? '' : 'hover:text-primary']"
        />
      </div>
    </UContainer>
    <USeparator color="secondary" />
    <slot />
  </UMain>

  <LayoutFooter />
</template>

<script setup lang="ts">
const pages = ref([
  { title: "Все курсы", path: "/courses" },
  { title: "Категории", path: "/courses/categories" },
]);
</script>
