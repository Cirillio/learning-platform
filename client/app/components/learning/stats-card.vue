<script setup lang="ts">
interface Props {
  icon: string;
  iconColor: string;
  bgColor: string;
  value: string | number;
  label: string;
  link?: {
    to: string;
    text: string;
  };
}

defineProps<Props>();
</script>

<template>
  <div class="bg-elevated rounded-xl p-5 border border-default">
    <div class="flex items-center justify-between mb-3">
      <span class="text-sm text-muted">{{ label }}</span>
      <UIcon :name="icon" :class="['size-5', iconColor]" />
    </div>
    <div class="text-2xl font-bold text-default">{{ value }}</div>
    <NuxtLink
      v-if="link"
      :to="link.to"
      class="text-xs text-primary hover:underline mt-1 inline-block"
    >
      {{ link.text }}
    </NuxtLink>
    <p v-else class="text-xs text-muted mt-1">
      <slot name="subtitle" />
    </p>
  </div>
</template>
