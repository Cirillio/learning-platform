<script lang="ts" setup></script>

<template>
  <NuxtLink
    to="/"
    class="flex items-center justify-center bg-default hover:*:text-secondary border border-muted hover:border-secondary/50 transition-all duration-150 rounded-sm font-semibold p-2.5"
    :class="{ 'border-primary': $route.path === '/' }"
  >
    <UIcon
      name="i-heroicons-command-line"
      class="size-8 text-primary transition-all duration-150"
    />
  </NuxtLink>
</template>
