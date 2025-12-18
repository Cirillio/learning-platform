<script setup lang="ts">
import type { LessonDetail, Assignment, Submission } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Просмотр урока",
});

const route = useRoute();
const router = useRouter();
const api = useApi();
const toast = useToast();

const courseSlug = computed(() => route.params.slug as string);
const lessonSlug = computed(() => route.params.lesson_slug as string);

// Fetch lesson
const { data: lesson, status: lessonStatus } = await useAsyncData<LessonDetail>(
  `teacher-lesson-${lessonSlug.value}`,
  () => api.get<LessonDetail>(`/lessons/${lessonSlug.value}/`)
);

// Fetch assignments for this lesson
interface AssignmentsResponse {
  count: number;
  results: Assignment[];
}

const { data: assignmentsData, status: assignmentsStatus } =
  await useAsyncData<AssignmentsResponse>(
    `teacher-lesson-assignments-${lessonSlug.value}`,
    () =>
      api.get<AssignmentsResponse>("/assignments/", {
        lesson: lessonSlug.value,
      })
  );

const assignments = computed(() => assignmentsData.value?.results || []);

// Fetch submissions for lesson assignments
interface SubmissionsResponse {
  count: number;
  results: Submission[];
}

const { data: submissionsData } = await useAsyncData<SubmissionsResponse>(
  `teacher-lesson-submissions-${lessonSlug.value}`,
  async () => {
    // Получаем все сдачи для всех заданий урока
    if (assignments.value.length === 0) {
      return { count: 0, results: [] };
    }

    // Собираем submissions со всех заданий параллельно
    const submissionsPromises = assignments.value.map((assignment) =>
      api.get<SubmissionsResponse>("/submissions/", {
        assignment: assignment.id.toString(),
      })
    );

    const submissionsResults = await Promise.all(submissionsPromises);

    // Объединяем все результаты
    const allSubmissions = submissionsResults.flatMap((res) => res.results);

    return {
      count: allSubmissions.length,
      results: allSubmissions,
    };
  },
  { watch: [assignments] }
);

const submissions = computed(() => submissionsData.value?.results || []);

// Group submissions by assignment
const submissionsByAssignment = computed(() => {
  const grouped: Record<number, Submission[]> = {};
  for (const sub of submissions.value) {
    const assignmentId = sub.assignment;
    if (!grouped[assignmentId]) {
      grouped[assignmentId] = [];
    }
    grouped[assignmentId]!.push(sub);
  }
  return grouped;
});

// Stats
const pendingSubmissions = computed(
  () => submissions.value.filter((s) => s.status === "pending").length
);

const gradedSubmissions = computed(
  () => submissions.value.filter((s) => s.status === "graded").length
);

// Delete lesson
const handleDelete = async () => {
  if (
    !confirm(
      "Вы уверены, что хотите удалить этот урок? Все материалы и задания также будут удалены."
    )
  )
    return;

  try {
    await api.delete(`/lessons/${lessonSlug.value}/`);
    toast.add({ title: "Урок удален", color: "success" });
    router.push(`/teacher/courses/${courseSlug.value}/lessons`);
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
    month: "short",
    year: "numeric",
  });
};

// Format file size
const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
};
</script>

<template>
  <div class="space-y-6">
    <!-- Loading -->
    <div v-if="lessonStatus === 'pending'" class="space-y-6">
      <USkeleton class="h-32 rounded-xl" />
      <USkeleton class="h-64 rounded-xl" />
    </div>

    <!-- Error -->
    <div v-else-if="!lesson" class="text-center py-20">
      <UIcon
        name="i-lucide-alert-circle"
        class="size-16 text-error mx-auto mb-4"
      />
      <h2 class="text-xl font-semibold mb-2">Урок не найден</h2>
      <UButton :to="`/teacher/courses/${courseSlug}/lessons`" color="primary">
        К списку уроков
      </UButton>
    </div>

    <!-- Content -->
    <template v-else>
      <!-- Header -->
      <div class="flex items-start justify-between gap-4">
        <div class="flex-1">
          <div class="flex items-center gap-3 mb-2">
            <UBadge color="primary" variant="soft" size="lg">
              Урок {{ lesson.order }}
            </UBadge>
            <UBadge
              v-if="!lesson.is_published"
              color="warning"
              variant="soft"
              size="lg"
            >
              Черновик
            </UBadge>
            <UBadge v-else color="success" variant="soft" size="lg">
              Опубликован
            </UBadge>
          </div>
          <h1 class="text-3xl font-bold text-default mb-2">
            {{ lesson.title }}
          </h1>
          <p class="text-lg text-muted">
            {{ lesson.description }}
          </p>
          <div class="flex items-center gap-4 mt-3 text-sm text-muted">
            <span class="flex items-center gap-1">
              <UIcon name="i-lucide-clock" class="size-4" />
              {{ lesson.duration_minutes }} мин
            </span>
            <span class="flex items-center gap-1">
              <UIcon name="i-lucide-paperclip" class="size-4" />
              {{ lesson.materials?.length || 0 }} материалов
            </span>
            <span class="flex items-center gap-1">
              <UIcon name="i-lucide-clipboard-list" class="size-4" />
              {{ assignments.length }} заданий
            </span>
          </div>
        </div>
        <div class="flex gap-2 shrink-0">
          <UButton
            color="neutral"
            variant="ghost"
            icon="i-lucide-arrow-left"
            :to="`/teacher/courses/${courseSlug}/lessons`"
          >
            Назад
          </UButton>
          <UButton
            color="primary"
            icon="i-lucide-pencil"
            :to="`/teacher/courses/${courseSlug}/lessons/${lessonSlug}/edit`"
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

      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <UCard>
          <div class="flex items-center gap-3">
            <div class="p-2 bg-primary/10 rounded-lg">
              <UIcon
                name="i-lucide-clipboard-list"
                class="size-5 text-primary"
              />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ assignments.length }}</div>
              <div class="text-sm text-muted">Заданий</div>
            </div>
          </div>
        </UCard>
        <UCard>
          <div class="flex items-center gap-3">
            <div class="p-2 bg-warning/10 rounded-lg">
              <UIcon name="i-lucide-clock" class="size-5 text-warning" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ pendingSubmissions }}</div>
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
              <div class="text-2xl font-bold">{{ gradedSubmissions }}</div>
              <div class="text-sm text-muted">Проверено</div>
            </div>
          </div>
        </UCard>
        <UCard>
          <div class="flex items-center gap-3">
            <div class="p-2 bg-info/10 rounded-lg">
              <UIcon name="i-lucide-file-text" class="size-5 text-info" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ submissions.length }}</div>
              <div class="text-sm text-muted">Всего сдач</div>
            </div>
          </div>
        </UCard>
      </div>

      <!-- Video -->
      <UCard v-if="lesson.video_url">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-video" class="size-5 text-primary" />
            <h3 class="font-semibold">Видео урока</h3>
          </div>
        </template>
        <div class="aspect-video rounded-lg overflow-hidden bg-elevated">
          <iframe
            v-if="lesson.video_url.includes('youtube')"
            :src="lesson.video_url.replace('watch?v=', 'embed/')"
            class="w-full h-full"
            frameborder="0"
            allowfullscreen
          />
          <video
            v-else
            :src="lesson.video_url"
            controls
            class="w-full h-full"
          />
        </div>
      </UCard>

      <!-- Content -->
      <UCard v-if="lesson.content">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-file-text" class="size-5 text-primary" />
            <h3 class="font-semibold">Содержание урока</h3>
          </div>
        </template>
        <LessonsContentViewer
          :title="lesson.title"
          :content="lesson.content"
          :duration="lesson.duration_minutes"
        />
      </UCard>

      <!-- Materials -->
      <UCard v-if="lesson.materials && lesson.materials.length > 0">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-paperclip" class="size-5 text-primary" />
            <h3 class="font-semibold">
              Материалы ({{ lesson.materials.length }})
            </h3>
          </div>
        </template>
        <div class="space-y-2">
          <div
            v-for="material in lesson.materials"
            :key="material.id"
            class="flex items-center justify-between p-3 bg-elevated rounded-lg hover:bg-muted/50 transition-colors"
          >
            <div class="flex items-center gap-3">
              <div class="p-2 bg-primary/10 rounded-lg">
                <UIcon name="i-lucide-file" class="size-5 text-primary" />
              </div>
              <div>
                <div class="font-medium">{{ material.title }}</div>
                <div class="text-xs text-muted">
                  {{ formatFileSize(material.file_size) }}
                </div>
              </div>
            </div>
            <UButton
              :to="material.file_url"
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

      <!-- Assignments with Submissions -->
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

      <!-- Comments -->
      <ClientOnly>
        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon
                name="i-lucide-message-circle"
                class="size-5 text-primary"
              />
              <h3 class="font-semibold">Комментарии</h3>
            </div>
          </template>
          <CommentsList :lesson-id="lesson.id" />
        </UCard>
      </ClientOnly>
    </template>
  </div>
</template>
