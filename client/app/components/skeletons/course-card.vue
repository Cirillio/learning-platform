<template>
  <UCard
    :ui="{
      root: '!ring-primary/25',
    }"
  >
    <div class="space-y-1">
      <!-- Категория -->
      <USkeleton class="h-5 w-24" />

      <!-- Заголовок -->
      <div class="space-y-2">
        <USkeleton class="h-6 w-3/4" />
        <USkeleton class="h-6 w-full" />
      </div>

      <!-- Описание -->
      <div class="space-y-2">
        <USkeleton class="h-4 w-full" />
        <USkeleton class="h-4 w-5/6" />
      </div>

      <!-- Преподаватель -->
      <div class="flex items-center gap-2 pt-2">
        <USkeleton class="size-6 rounded-full" />
        <USkeleton class="h-4 w-32" />
      </div>
    </div>
  </UCard>
</template>
