<script lang="ts" setup>
const props = withDefaults(
  defineProps<{
    label?: string;
    size?: "sm" | "md" | "lg" | "xl" | "2xl" | "3xl";
  }>(),
  {
    size: "lg",
  }
);
</script>

<template>
  <NuxtLink
    to="/"
    class="flex items-center gap-2.5 justify-center bg-default hover:*:text-secondary border border-muted hover:border-secondary/50 transition-all duration-150 rounded-sm font-semibold p-2.5"
    :class="{ 'border-primary': $route.path === '/' }"
  >
    <UIcon
      name="i-heroicons-command-line"
      class="text-primary transition-all duration-150"
      :class="{
        'size-8': size === 'lg',
        'size-4': size === 'sm',
        'size-6': size === 'md',
        'size-10': size === 'xl',
        'size-12': size === '2xl',
        'size-16': size === '3xl',
      }"
    />

    <span
      v-if="label"
      class="font-semibold"
      :class="{
        'text-md': size === 'sm',
        'text-lg': size === 'md',
        'text-xl': size === 'lg',
        'text-2xl': size === 'xl',
        'text-3xl': size === '2xl',
        'text-4xl': size === '3xl',
      }"
    >
      {{ label }}</span
    >
  </NuxtLink>
</template>
