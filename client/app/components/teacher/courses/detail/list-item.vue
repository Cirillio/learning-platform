<script lang="ts" setup>
interface Props {
  order?: number;
  title?: string;
  desc: string;
  subdesc?: string;
  link?: string;
}

defineProps<Props>();

const emit = defineEmits<{
  (e: "edit"): void;
  (e: "delete"): void;
}>();
</script>

<template>
  <UCard
    :ui="{
      root: 'group',
      body: 'flex items-center gap-3',
    }"
  >
    <!-- Leading -->
    <slot name="leading"></slot>

    <!-- Info -->
    <div class="flex-1 min-w-0">
      <div class="flex items-center gap-2 mb-1">
        <slot name="title">
          <h3 class="text-3xl font-semibold text-default">{{ title }}</h3>
        </slot>
      </div>
      <p class="text-base text-muted truncate">{{ desc }}</p>
    </div>

    <!-- Duration -->
    <div class="text-base text-muted shrink-0">
      {{ subdesc }}
    </div>

    <!-- Actions -->
    <div class="flex items-center gap-1">
      <UButton
        v-if="link"
        :to="link"
        icon="i-lucide-external-link"
        color="neutral"
        variant="ghost"
        size="lg"
      />
      <UButton
        icon="i-lucide-pencil"
        color="neutral"
        variant="ghost"
        size="lg"
        @click="emit('edit')"
      />
      <UButton
        icon="i-lucide-trash-2"
        color="error"
        variant="ghost"
        size="lg"
        @click="emit('delete')"
      />
    </div>
  </UCard>
</template>
