<script setup lang="ts">
import { formatDate, formatFileSize } from "~/utils/formatters.util";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Просмотр задания",
});

const {
  courseSlug,
  assignmentId,
  assignment,
  assignmentStatus,
  lesson,
  submissions,
  pendingCount,
  gradedCount,
  lateCount,
  isDueDatePassed,
  handleDelete,
} = useTeacherAssignment();
</script>

<template>
  <div class="space-y-6">
    <!-- Loading -->
    <div v-if="assignmentStatus === 'pending'" class="space-y-6">
      <USkeleton class="h-32 rounded-xl" />
      <USkeleton class="h-64 rounded-xl" />
    </div>

    <!-- Error -->
    <div v-else-if="!assignment" class="text-center py-20">
      <UIcon
        name="i-lucide-alert-circle"
        class="size-16 text-error mx-auto mb-4"
      />
      <h2 class="text-xl font-semibold mb-2">Задание не найдено</h2>
      <UButton
        :to="`/teacher/courses/${courseSlug}/assignments`"
        color="primary"
      >
        К списку заданий
      </UButton>
    </div>

    <!-- Content -->
    <template v-else>
      <!-- Header -->
      <div class="flex items-start justify-between gap-4">
        <div class="flex-1">
          <div class="flex items-center gap-3 mb-2">
            <UBadge
              v-if="assignment.is_required"
              color="error"
              variant="soft"
              size="lg"
            >
              Обязательное
            </UBadge>
            <UBadge v-else color="neutral" variant="soft" size="lg">
              Необязательное
            </UBadge>
            <UBadge color="primary" variant="soft" size="lg">
              {{ assignment.max_score }} баллов
            </UBadge>
            <UBadge
              v-if="isDueDatePassed"
              color="error"
              variant="soft"
              size="lg"
            >
              Срок истёк
            </UBadge>
          </div>
          <h1 class="text-3xl font-bold text-default mb-2">
            {{ assignment.title }}
          </h1>
          <p class="text-lg text-muted">
            {{ assignment.description }}
          </p>
        </div>
        <div class="flex gap-2 shrink-0">
          <UButton
            color="neutral"
            variant="ghost"
            icon="i-lucide-arrow-left"
            :to="`/teacher/courses/${courseSlug}/assignments`"
          >
            Назад
          </UButton>
          <UButton
            color="primary"
            icon="i-lucide-pencil"
            :to="`/teacher/courses/${courseSlug}/assignments/${assignmentId}/edit`"
          >
            Редактировать
          </UButton>
          <UButton
            color="error"
            variant="ghost"
            icon="i-lucide-trash-2"
            @click="handleDelete"
          />
        </div>
      </div>

      <!-- Lesson Info Card -->
      <UCard v-if="lesson" class="bg-primary/5 border-primary/20">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-primary/10 rounded-lg">
            <UIcon name="i-lucide-book-open" class="size-6 text-primary" />
          </div>
          <div class="flex-1">
            <div class="text-sm text-muted mb-1">Урок</div>
            <NuxtLink
              :to="`/teacher/courses/${courseSlug}/lessons/${lesson.slug}`"
              class="text-lg font-semibold text-default hover:text-primary transition-colors"
            >
              {{ lesson.order }}. {{ lesson.title }}
            </NuxtLink>
            <p
              v-if="lesson.description"
              class="text-sm text-muted mt-1 line-clamp-2"
            >
              {{ lesson.description }}
            </p>
          </div>
          <UButton
            :to="`/teacher/courses/${courseSlug}/lessons/${lesson.slug}`"
            color="primary"
            variant="soft"
            icon="i-lucide-external-link"
            size="sm"
          >
            Перейти к уроку
          </UButton>
        </div>
      </UCard>

      <!-- Quick Stats -->
      <TeacherAssignmentsAssignmentStats
        :total-count="submissions.length"
        :pending-count="pendingCount"
        :graded-count="gradedCount"
        :late-count="lateCount"
      />

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Instructions -->
          <UCard>
            <template #header>
              <div class="flex items-center gap-2">
                <UIcon name="i-lucide-file-text" class="size-5 text-primary" />
                <h3 class="font-semibold">Инструкции</h3>
              </div>
            </template>
            <div
              class="prose prose-neutral dark:prose-invert max-w-none whitespace-pre-wrap"
            >
              {{ assignment.instructions || "Инструкции не указаны" }}
            </div>
          </UCard>

          <!-- Files -->
          <UCard v-if="assignment.files && assignment.files.length > 0">
            <template #header>
              <div class="flex items-center gap-2">
                <UIcon name="i-lucide-paperclip" class="size-5 text-primary" />
                <h3 class="font-semibold">
                  Файлы задания ({{ assignment.files.length }})
                </h3>
              </div>
            </template>
            <div class="space-y-2">
              <div
                v-for="file in assignment.files"
                :key="file.id"
                class="flex items-center justify-between p-3 bg-elevated rounded-lg hover:bg-muted/50 transition-colors"
              >
                <div class="flex items-center gap-3">
                  <div class="p-2 bg-primary/10 rounded-lg">
                    <UIcon name="i-lucide-file" class="size-5 text-primary" />
                  </div>
                  <div>
                    <div class="font-medium">{{ file.filename }}</div>
                    <div class="text-xs text-muted">
                      {{ formatFileSize(file.file_size) }}
                    </div>
                  </div>
                </div>
                <UButton
                  :to="file.file_url"
                  target="_blank"
                  color="neutral"
                  variant="ghost"
                  icon="i-lucide-download"
                  size="sm"
                >
                  Скачать
                </UButton>
              </div>
            </div>
          </UCard>

          <!-- Submissions -->
          <TeacherAssignmentsSubmissionsList :submissions="submissions" />
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Info Card -->
          <UCard>
            <template #header>
              <div class="flex items-center gap-2">
                <UIcon name="i-lucide-info" class="size-5 text-primary" />
                <h3 class="font-semibold">Информация</h3>
              </div>
            </template>
            <div class="space-y-4 text-sm">
              <div class="flex justify-between items-center">
                <span class="text-muted">Макс. балл</span>
                <span class="font-semibold">{{ assignment.max_score }}</span>
              </div>
              <USeparator />
              <div class="flex justify-between items-center">
                <span class="text-muted">Срок сдачи</span>
                <span
                  :class="
                    isDueDatePassed
                      ? 'text-error font-semibold'
                      : 'font-semibold'
                  "
                >
                  {{ formatDate(assignment.due_date) }}
                </span>
              </div>
              <USeparator />
              <div class="flex justify-between items-center">
                <span class="text-muted">Поздняя сдача</span>
                <UBadge
                  :color="
                    assignment.allow_late_submission ? 'success' : 'error'
                  "
                  variant="soft"
                  size="sm"
                >
                  {{
                    assignment.allow_late_submission ? "Разрешена" : "Запрещена"
                  }}
                </UBadge>
              </div>
              <USeparator />
              <div class="flex justify-between items-center">
                <span class="text-muted">Обязательное</span>
                <UBadge
                  :color="assignment.is_required ? 'error' : 'neutral'"
                  variant="soft"
                  size="sm"
                >
                  {{ assignment.is_required ? "Да" : "Нет" }}
                </UBadge>
              </div>
              <USeparator />
              <div class="flex justify-between items-center">
                <span class="text-muted">Создано</span>
                <span class="font-medium">{{
                  new Date(assignment.created_at).toLocaleDateString("ru-RU")
                }}</span>
              </div>
            </div>
          </UCard>

          <!-- Quick Actions -->
          <UCard>
            <template #header>
              <div class="flex items-center gap-2">
                <UIcon name="i-lucide-zap" class="size-5 text-primary" />
                <h3 class="font-semibold">Быстрые действия</h3>
              </div>
            </template>
            <div class="space-y-2">
              <UButton
                :to="`/teacher/courses/${courseSlug}/assignments/${assignmentId}/edit`"
                color="neutral"
                variant="soft"
                icon="i-lucide-pencil"
                block
              >
                Редактировать задание
              </UButton>
              <UButton
                v-if="lesson"
                :to="`/teacher/courses/${courseSlug}/lessons/${lesson.slug}`"
                color="neutral"
                variant="soft"
                icon="i-lucide-book-open"
                block
              >
                Перейти к уроку
              </UButton>
              <UButton
                :to="`/teacher/courses/${courseSlug}/assignments`"
                color="neutral"
                variant="ghost"
                icon="i-lucide-list"
                block
              >
                Все задания курса
              </UButton>
            </div>
          </UCard>
        </div>
      </div>
    </template>
  </div>
</template>
