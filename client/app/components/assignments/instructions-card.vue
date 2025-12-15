<script setup lang="ts">
defineProps<{
  instructions: string;
}>();
</script>

<template>
  <UCard>
    <template #header>
      <h2 class="text-2xl font-semibold text-default flex items-center gap-2">
        <UIcon name="i-lucide-file-text" class="size-6 text-primary" />
        Инструкции
      </h2>
    </template>
    <div class="text-lg px-3 max-w-none text-muted" v-html="instructions" />
  </UCard>
</template>
