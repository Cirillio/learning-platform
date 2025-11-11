<script lang="ts" setup></script>

<template>
  <div class="flex rounded-full bg-elevated gap-1.5 p-1.5 items-center">
    <UButton
      to="/auth/login"
      variant="ghost"
      color="primary"
      size="lg"
      icon="heroicons-arrow-right-end-on-rectangle-16-solid"
      class="hidden sm:inline-flex"
    />

    <UButton
      size="lg"
      to="/auth/register"
      color="secondary"
      icon="i-heroicons-user-plus-solid"
    />
  </div>
</template>
