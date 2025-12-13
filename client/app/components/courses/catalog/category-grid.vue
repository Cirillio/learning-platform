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

  <div
    v-else-if="categories"
    class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-2 mt-8"
  >
    <UCard
      v-for="category in categories"
      :key="category.id"
      class="flex flex-col h-full hover:ring hover:ring-primary-500 transition-all duration-200"
      :ui="{
        header: '!p-0',
        body: 'py-2! px-4! h-full border-0',
        footer: 'px-4! mt-auto',
      }"
    >
      <template #header>
        <div
          class="flex items-center justify-center h-60 bg-elevated overflow-hidden"
        >
          <NuxtImg
            v-if="category.icon"
            :src="category.icon"
            class="object-cover object-top h-full w-full"
          />
          <UIcon
            v-else
            name="i-heroicons-academic-cap"
            class="h-24 w-24 text-muted"
          />
        </div>
      </template>

      <div class="flex flex-col gap-1">
        <h3 class="text-2xl font-bold text-default">
          {{ category.name }}
        </h3>
        <p class="text-sm text-muted line-clamp-3">
          {{ category.description }}
        </p>
      </div>

      <template #footer>
        <UButton
          :to="`/courses?category=${category.slug}`"
          label="Смотреть курсы"
          color="primary"
          variant="ghost"
          block
          size="lg"
          icon="i-heroicons-arrow-right-20-solid"
          trailing
        />
      </template>
    </UCard>
  </div>
</template>
