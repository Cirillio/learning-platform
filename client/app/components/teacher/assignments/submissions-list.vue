<script setup lang="ts">
import type { Submission } from "~/types";

defineProps<{
  submissions: Submission[];
}>();
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <UIcon name="i-lucide-users" class="size-5 text-primary" />
          <h3 class="font-semibold">
            Сдачи студентов ({{ submissions.length }})
          </h3>
        </div>
      </div>
    </template>

    <!-- Empty -->
    <div v-if="submissions.length === 0" class="text-center py-8">
      <UIcon
        name="i-lucide-inbox"
        class="size-12 text-muted mx-auto mb-3"
      />
      <p class="text-muted">Пока никто не сдал это задание</p>
    </div>

    <!-- Submissions List -->
    <div v-else class="divide-y divide-default">
      <div
        v-for="submission in submissions"
        :key="submission.id"
        class="p-4 flex items-center justify-between hover:bg-muted/30 transition-colors"
      >
        <div class="flex items-center gap-3">
          <UAvatar :alt="submission.student_name" size="md" />
          <div>
            <div class="font-medium">{{ submission.student_name }}</div>
            <div class="text-sm text-muted">
              {{
                new Date(submission.submitted_at).toLocaleString(
                  "ru-RU"
                )
              }}
              <span v-if="submission.is_late" class="text-error ml-1"
                >(просрочено)</span
              >
            </div>
            <div
              v-if="submission.content"
              class="text-sm text-muted mt-1 line-clamp-1"
            >
              {{ submission.content }}
            </div>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-2">
            <UIcon
              v-if="submission.files_count"
              name="i-lucide-paperclip"
              class="size-4 text-muted"
            />
            <span
              v-if="submission.files_count"
              class="text-sm text-muted"
              >{{ submission.files_count }}</span
            >
          </div>
          <UBadge
            :color="
              submission.status === 'pending'
                ? 'warning'
                : submission.status === 'graded'
                ? 'success'
                : 'info'
            "
            variant="soft"
          >
            {{
              submission.status === "pending"
                ? "Ожидает"
                : submission.status === "graded"
                ? "Оценено"
                : "Возвращено"
            }}
          </UBadge>
          <UButton
            :to="`/teacher/grading/${submission.id}`"
            color="primary"
            variant="soft"
            icon="i-lucide-eye"
            size="sm"
          >
            {{
              submission.status === "pending"
                ? "Проверить"
                : "Подробнее"
            }}
          </UButton>
        </div>
      </div>
    </div>
  </UCard>
</template>
