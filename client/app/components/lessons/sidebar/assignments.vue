<script setup lang="ts">
interface Props {
  lessonSlug: string;
  assignmentsCount: number;
}

defineProps<Props>();

const route = useRoute();
const courseSlug = computed(() => route.params.slug as string);
</script>

<template>
  <UCard class="dark:bg-muted/25 bg-muted/75">
    <!-- Header -->
    <div class="p-4 border-b border-default">
      <div class="flex items-center gap-3">
        <div
          class="size-10 rounded-lg bg-warning/10 flex items-center justify-center"
        >
          <UIcon name="i-lucide-clipboard-list" class="size-5 text-warning" />
        </div>
        <div>
          <h3 class="font-semibold text-default">Задания</h3>
          <p class="text-sm text-muted">
            {{ assignmentsCount }}
            {{ assignmentsCount === 1 ? "задание" : "заданий" }}
          </p>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="p-4 space-y-3">
      <p class="text-sm text-muted">
        К этому уроку есть практические задания для закрепления материала.
      </p>

      <UButton
        :to="`/courses/${courseSlug}/lessons/${lessonSlug}/assignments`"
        variant="soft"
        color="warning"
        icon="i-lucide-pen-tool"
        block
      >
        Перейти к заданиям
      </UButton>
    </div>
  </UCard>
</template>
