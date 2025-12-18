<script setup lang="ts">
import type { Assignment, LessonDetail, Submission } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Просмотр задания",
});

const route = useRoute();
const router = useRouter();
const api = useApi();
const toast = useToast();

const courseSlug = computed(() => route.params.slug as string);
const assignmentId = computed(() => route.params.id as string);

// Fetch assignment
const { data: assignment, status: assignmentStatus } =
  await useAsyncData<Assignment>(
    `teacher-assignment-${assignmentId.value}`,
    () => api.get<Assignment>(`/assignments/${assignmentId.value}/`)
  );

// Fetch lesson info
const { data: lesson } = await useAsyncData<LessonDetail | null>(
  `teacher-assignment-lesson-${assignmentId.value}`,
  async () => {
    if (!assignment.value?.lesson) return null;
    try {
      return await api.get<LessonDetail>(
        `/lessons/${assignment.value.lesson}/`
      );
    } catch {
      return null;
    }
  },
  { watch: [assignment] }
);

// Fetch submissions for this assignment
interface SubmissionsResponse {
  count: number;
  results: Submission[];
}

const { data: submissionsData, refresh: refreshSubmissions } =
  await useAsyncData<SubmissionsResponse>(
    `teacher-assignment-submissions-${assignmentId.value}`,
    () =>
      api.get<SubmissionsResponse>("/submissions/", {
        assignment: assignmentId.value,
      })
  );

const submissions = computed(() => submissionsData.value?.results || []);

// Stats
const pendingCount = computed(
  () => submissions.value.filter((s) => s.status === "pending").length
);

const gradedCount = computed(
  () => submissions.value.filter((s) => s.status === "graded").length
);

const lateCount = computed(
  () => submissions.value.filter((s) => s.is_late).length
);

// Delete assignment
const handleDelete = async () => {
  if (
    !confirm(
      "Вы уверены, что хотите удалить это задание? Все сдачи студентов также будут удалены."
    )
  )
    return;

  try {
    await api.delete(`/assignments/${assignmentId.value}/`);
    toast.add({ title: "Задание удалено", color: "success" });
    router.push(`/teacher/courses/${courseSlug.value}/assignments`);
  } catch (e) {
    toast.add({
      title: "Ошибка удаления",
      description: (e as Error).message,
      color: "error",
    });
  }
};

// Format date
const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return "Без срока";
  return new Date(dateString).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

// Format file size
const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
};

// Check if due date passed
const isDueDatePassed = computed(() => {
  if (!assignment.value?.due_date) return false;
  return new Date(assignment.value.due_date) < new Date();
});
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
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <UCard>
          <div class="flex items-center gap-3">
            <div class="p-2 bg-primary/10 rounded-lg">
              <UIcon name="i-lucide-file-text" class="size-5 text-primary" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ submissions.length }}</div>
              <div class="text-sm text-muted">Всего сдач</div>
            </div>
          </div>
        </UCard>
        <UCard>
          <div class="flex items-center gap-3">
            <div class="p-2 bg-warning/10 rounded-lg">
              <UIcon name="i-lucide-clock" class="size-5 text-warning" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ pendingCount }}</div>
              <div class="text-sm text-muted">Ожидают проверки</div>
            </div>
          </div>
        </UCard>
        <UCard>
          <div class="flex items-center gap-3">
            <div class="p-2 bg-success/10 rounded-lg">
              <UIcon name="i-lucide-check-circle" class="size-5 text-success" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ gradedCount }}</div>
              <div class="text-sm text-muted">Проверено</div>
            </div>
          </div>
        </UCard>
        <UCard>
          <div class="flex items-center gap-3">
            <div class="p-2 bg-error/10 rounded-lg">
              <UIcon name="i-lucide-alert-triangle" class="size-5 text-error" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ lateCount }}</div>
              <div class="text-sm text-muted">Просрочено</div>
            </div>
          </div>
        </UCard>
      </div>

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
