<script lang="ts" setup>
interface Props {
  icon: string; // This is not used in the template, consider removing or using it.
  value: number;
  label: string;
  color: string;
}

defineProps<Props>();
</script>

<template>
  <UCard
    class="shadow-sm"
    :ui="{
      body: 'flex size-full',
    }"
  >
    <div class="text-center flex flex-col justify-between size-full">
      <div
        class="size-16 rounded-xl flex items-center justify-center"
        :class="'bg-' + color + '/10'"
      >
        <UIcon :name="icon" class="size-8" :class="'text-' + color" />
      </div>
      <span class="flex items-baseline justify-between">
        <p class="text-5xl font-bold text-default">
          {{ value }}
        </p>
        <p class="text-lg text-muted">{{ label }}</p>
      </span>
    </div>
  </UCard>
</template>
