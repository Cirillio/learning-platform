<script setup lang="ts">
interface Props {
  description: string;
}

defineProps<Props>();
</script>

<template>
  <!-- Trusted By (Mockup placeholder) -->
  <UCard class="bg-default! dark:bg-default! p-2">
    <div class="flex flex-col gap-6">
      <h3 class="font-bold text-2xl text-neutral-900 dark:text-primary">
        Этот курс выбирают сотрудники компаний
      </h3>
      <div
        class="flex flex-wrap gap-12 select-none opacity-60 *:hover:text-primary *:transition-colors"
      >
        <!-- Placeholders for logos -->
        <span class="font-bold text-3xl">Google</span>
        <span class="font-bold text-3xl">Amazon</span>
        <span class="font-bold text-3xl">Netflix</span>
        <span class="font-bold text-3xl">Spotify</span>
      </div>
    </div>
  </UCard>

  <!-- Description -->
  <div class="space-y-4">
    <h2 class="text-3xl font-bold text-neutral-900 dark:text-white">
      Описание
    </h2>
    <div
      class="prose dark:prose-invert text-lg max-w-none text-neutral-600 dark:text-neutral-300"
    >
      {{ description }}
    </div>
  </div>
</template>
