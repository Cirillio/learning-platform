<script setup lang="ts">
import type { Assignment, Submission } from "~/types";
import { formatDate } from "~/utils/formatters.util";

defineProps<{
  assignments: Assignment[];
  submissionsByAssignment: Record<number, Submission[]>;
  courseSlug: string;
  lessonSlug: string;
}>();
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <UIcon
            name="i-lucide-clipboard-list"
            class="size-5 text-primary"
          />
          <h3 class="font-semibold">
            Задания урока ({{ assignments.length }})
          </h3>
        </div>
        <UButton
          :to="`/teacher/courses/${courseSlug}/assignments/create?lesson=${lessonSlug}`"
          icon="i-lucide-plus"
          color="primary"
          size="sm"
        >
          Добавить задание
        </UButton>
      </div>
    </template>

    <!-- Empty -->
    <div v-if="assignments.length === 0" class="text-center py-8">
      <UIcon
        name="i-lucide-clipboard-x"
        class="size-12 text-muted mx-auto mb-3"
      />
      <p class="text-muted mb-4">Заданий пока нет</p>
      <UButton
        :to="`/teacher/courses/${courseSlug}/assignments/create?lesson=${lessonSlug}`"
        icon="i-lucide-plus"
        color="primary"
      >
        Добавить первое задание
      </UButton>
    </div>

    <!-- Assignments List -->
    <div v-else class="space-y-4">
      <div
        v-for="assignment in assignments"
        :key="assignment.id"
        class="border border-default rounded-lg overflow-hidden"
      >
        <!-- Assignment Header -->
        <div class="p-4 bg-elevated flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-warning/10 rounded-lg">
              <UIcon
                name="i-lucide-clipboard-list"
                class="size-5 text-warning"
              />
            </div>
            <div>
              <div class="flex items-center gap-2">
                <NuxtLink
                  :to="`/teacher/courses/${courseSlug}/assignments/${assignment.id}`"
                  class="font-semibold text-default hover:text-primary transition-colors"
                >
                  {{ assignment.title }}
                </NuxtLink>
                <UBadge
                  v-if="assignment.is_required"
                  color="error"
                  variant="soft"
                  size="xs"
                >
                  Обязательное
                </UBadge>
              </div>
              <div class="text-sm text-muted">
                {{ assignment.max_score }} баллов • Срок:
                {{ formatDate(assignment.due_date) }}
              </div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <UBadge color="neutral" variant="soft">
              {{ submissionsByAssignment[assignment.id]?.length || 0 }} сдач
            </UBadge>
            <UButton
              :to="`/teacher/courses/${courseSlug}/assignments/${assignment.id}/edit`"
              color="neutral"
              variant="ghost"
              icon="i-lucide-pencil"
              size="xs"
            />
          </div>
        </div>

        <!-- Submissions List -->
        <div
          v-if="submissionsByAssignment[assignment.id]?.length"
          class="divide-y divide-default"
        >
          <div
            v-for="submission in submissionsByAssignment[assignment.id]"
            :key="submission.id"
            class="p-3 flex items-center justify-between hover:bg-muted/30 transition-colors"
          >
            <div class="flex items-center gap-3">
              <UAvatar :alt="submission.student_name" size="sm" />
              <div>
                <div class="font-medium text-sm">
                  {{ submission.student_name }}
                </div>
                <div class="text-xs text-muted">
                  {{
                    new Date(submission.submitted_at).toLocaleString(
                      "ru-RU"
                    )
                  }}
                  <span v-if="submission.is_late" class="text-error ml-1"
                    >(просрочено)</span
                  >
                </div>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <UBadge
                :color="
                  submission.status === 'pending'
                    ? 'warning'
                    : submission.status === 'graded'
                    ? 'success'
                    : 'info'
                "
                variant="soft"
                size="sm"
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
                variant="ghost"
                icon="i-lucide-eye"
                size="xs"
              >
                Проверить
              </UButton>
            </div>
          </div>
        </div>

        <!-- No Submissions -->
        <div v-else class="p-4 text-center text-sm text-muted">
          Пока никто не сдал это задание
        </div>
      </div>
    </div>
  </UCard>
</template>
