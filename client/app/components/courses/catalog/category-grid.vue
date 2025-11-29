<script lang="ts" setup>
import type { NuxtError } from "#app";
import type { Category } from "~/types";

defineProps<{
  categories: Category[] | undefined;
  loading: boolean;
  error: NuxtError<unknown> | null;
}>();
</script>

<template>
  <div v-if="loading" class="mt-8">
    <UPageGrid>
      <UCard v-for="i in 6" :key="i">
        <template #header>
          <USkeleton class="h-8 w-3/4" />
        </template>
        <USkeleton class="h-12 w-full" />
      </UCard>
    </UPageGrid>
  </div>

  <div v-else-if="error" class="mt-8">
    <UAlert
      icon="i-heroicons-exclamation-triangle"
      color="error"
      variant="soft"
      title="Ошибка!"
      :description="error.message"
    />
  </div>

  <div v-else-if="categories" class="grid grid-cols-4 gap-8 mt-8">
    <UCard v-for="category in categories" :key="category.id">
      <template #header>
        <NuxtImg :src="category.icon" class="" />
      </template>
      <div class="flex items-center gap-4">
        <h3 class="text-lg font-bold">{{ category.name }}</h3>
      </div>

      <p class="text-gray-500 dark:text-gray-400">{{ category.description }}</p>

      <template #footer>
        <UButton
          :to="`/courses/all?category=${category.slug}`"
          label="Смотреть курсы"
          color="primary"
          variant="solid"
          block
        />
      </template>
    </UCard>
  </div>
</template>
