<script setup lang="ts">
defineProps<{
  title?: string;
  icon?: string;
  backTo?: string;
  backText?: string;
}>();
</script>

<template>
  <div class="text-center py-20">
    <UIcon
      :name="icon || 'i-lucide-alert-circle'"
      class="size-16 text-error mx-auto mb-4"
    />
    <h2 class="text-xl font-semibold mb-2">
      {{ title || "Ничего не найдено" }}
    </h2>
    <slot />
    <UButton
      v-if="backTo"
      :to="backTo"
      color="primary"
      class="mt-4"
    >
      {{ backText || "Назад" }}
    </UButton>
  </div>
</template>
