<script setup lang="ts">
interface Props {
  description: string;
}

defineProps<Props>();
</script>

<template>
  <!-- Trusted By (Mockup placeholder) -->
  <UCard>
    <div class="flex flex-col gap-4">
      <h3 class="font-semibold text-neutral-900 dark:text-white">
        Этот курс выбирают сотрудники компаний
      </h3>
      <div
        class="flex flex-wrap gap-6 opacity-60 *:hover:text-primary *:transition-colors"
      >
        <!-- Placeholders for logos -->
        <span class="font-bold text-xl">Google</span>
        <span class="font-bold text-xl">Amazon</span>
        <span class="font-bold text-xl">Netflix</span>
        <span class="font-bold text-xl">Spotify</span>
      </div>
    </div>
  </UCard>

  <!-- Description -->
  <div class="space-y-4">
    <h2 class="text-2xl font-bold text-neutral-900 dark:text-white">
      Описание
    </h2>
    <div
      class="prose dark:prose-invert max-w-none text-neutral-600 dark:text-neutral-300"
    >
      {{ description }}
    </div>
  </div>
</template>
