<script setup lang="ts">
import type { Submission } from "~/types";

interface Props {
  submissions: Submission[];
  pending?: boolean;
  emptyText?: string;
  onUpdate: () => void;
}

withDefaults(defineProps<Props>(), {
  pending: false,
  emptyText: "Нет работ на проверке",
});
</script>

<template>
  <UCard class="shadow-sm">
    <div
      class="px-3.5 py-2 mb-2 border-b border-default flex items-center justify-between"
    >
      <h2 class="text-2xl font-semibold text-default">Ожидают проверки</h2>
      <NuxtLink
        to="/teacher/grading"
        class="text-lg text-primary hover:underline"
      >
        Все работы →
      </NuxtLink>
    </div>

    <!-- Loading -->
    <div v-if="pending" class="py-2 space-y-4">
      <USkeleton v-for="i in 3" :key="i" class="h-16 rounded-lg" />
    </div>

    <!-- Empty -->
    <div v-else-if="submissions.length === 0" class="p-12 text-center">
      <UIcon name="i-lucide-inbox" class="size-12 text-muted mx-auto mb-3" />
      <p class="text-muted">{{ emptyText }}</p>
      <UButton label="Обновить" @click="onUpdate" variant="soft" class="mt-4" />
    </div>

    <!-- List -->
    <div v-else class="space-y-1">
      <TeacherSubmissionsListItem
        v-for="submission in submissions"
        :key="submission.id"
        :submission="submission"
      />
    </div>
  </UCard>
</template>
