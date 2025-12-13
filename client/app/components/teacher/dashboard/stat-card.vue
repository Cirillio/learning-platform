<script lang="ts" setup>
export interface StatItem {
  label: string;
  value: string | number;
  icon: string;
  iconColor: string;
  bgColor: string;
  link?: {
    to: string;
    text: string;
  };
  subtitle?: string;
}

defineProps<{
  stat: StatItem;
}>();
</script>

<template>
  <UCard class="shadow-sm">
    <div class="flex items-center justify-between">
      <span class="text-xl font-semibold text-muted">{{ stat.label }}</span>
      <div
        class="size-9 rounded-lg flex items-center justify-center"
        :class="stat.bgColor"
      >
        <UIcon :name="stat.icon" :class="['size-6', stat.iconColor]" />
      </div>
    </div>
    <div class="text-4xl font-bold text-default">{{ stat.value }}</div>
    <NuxtLink
      v-if="stat.link"
      :to="stat.link.to"
      :class="['text-base hover:underline mt-3 inline-block', stat.iconColor]"
    >
      {{ stat.link.text }}
    </NuxtLink>
    <span
      v-else-if="stat.subtitle"
      class="text-base text-muted mt-3 inline-block"
    >
      {{ stat.subtitle }}
    </span>
  </UCard>
</template>
