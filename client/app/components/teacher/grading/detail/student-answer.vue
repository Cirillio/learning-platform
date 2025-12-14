<script setup lang="ts">
defineProps<{
  content: string | null;
}>();
</script>

<template>
  <UCard>
    <template #header>
      <h2 class="text-2xl font-semibold text-default">Ответ студента</h2>
    </template>
    <div v-if="content" class="prose text-lg text-default whitespace-pre-wrap">
      {{ content }}
    </div>
    <p v-else class="text-muted italic">Текстовый ответ не предоставлен</p>
  </UCard>
</template>
