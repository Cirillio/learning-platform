<script setup lang="ts">
defineProps<{
  instructions: string;
}>();
</script>

<template>
  <div class="bg-elevated rounded-xl border border-default p-6 lg:p-8">
    <h2 class="text-lg font-semibold text-default mb-4 flex items-center gap-2">
      <UIcon name="i-lucide-file-text" class="size-5 text-primary" />
      Инструкции
    </h2>
    <div class="prose prose-sm max-w-none text-muted" v-html="instructions" />
  </div>
</template>
