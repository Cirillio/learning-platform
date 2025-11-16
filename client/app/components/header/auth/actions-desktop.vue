<script lang="ts" setup></script>

<template>
  <div class="flex gap-1.5 items-center">
    <UButton
      to="/auth/login"
      variant="outline"
      color="secondary"
      size="lg"
      icon="heroicons:user-circle"
      class="hidden text-lg *:size-7 py-3 px-4 sm:inline-flex"
    />

    <UButton
      size="lg"
      to="/auth/register"
      color="primary"
      icon="heroicons:user-plus"
      class="text-lg py-3 px-4 *:size-7"
    />
  </div>
</template>
