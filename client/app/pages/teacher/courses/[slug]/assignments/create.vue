<script setup lang="ts">
import type { Lesson } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Создание задания",
});

const route = useRoute();
const router = useRouter();
const api = useApi();
const toast = useToast();

const courseSlug = computed(() => route.params.slug as string);
const isSubmitting = ref(false);

// Get pre-selected lesson from query params
const preselectedLesson = computed(
  () => route.query.lesson as string | undefined
);

// Fetch lessons for dropdown
interface LessonsResponse {
  count: number;
  results: Lesson[];
}

const { data: lessonsData, status } = await useAsyncData<LessonsResponse>(
  `teacher-course-lessons-${courseSlug.value}`,
  () => api.get<LessonsResponse>("/lessons/", { course: courseSlug.value })
);

const lessons = computed(() => lessonsData.value?.results || []);

// Form submit handler
const handleSubmit = async (formData: {
  lesson: string;
  title: string;
  description?: string;
  instructions?: string;
  max_score: number;
  due_date?: string | null;
  is_required: boolean;
  allow_late_submission: boolean;
}) => {
  isSubmitting.value = true;
  try {
    const newAssignment = await api.post<{ id: number }>(
      "/assignments/",
      formData
    );
    toast.add({
      title: "Задание создано",
      description: "Новое задание успешно добавлено",
      color: "success",
    });
    router.push(
      `/teacher/courses/${courseSlug.value}/assignments/${newAssignment.id}`
    );
  } catch (error) {
    toast.add({
      title: "Ошибка",
      description: (error as Error).message || "Не удалось создать задание",
      color: "error",
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Cancel handler
const handleCancel = () => {
  router.push(`/teacher/courses/${courseSlug.value}/assignments`);
};
</script>

<template>
  <div class="mx-auto max-w-3xl space-y-6">
    <!-- Loading -->
    <div v-if="status === 'pending'" class="space-y-6">
      <USkeleton class="h-12 w-64 rounded-lg" />
      <USkeleton class="h-6 w-48 rounded-lg" />
      <USkeleton class="h-[500px] rounded-xl" />
    </div>

    <!-- No Lessons Warning -->
    <div v-else-if="lessons.length === 0" class="text-center py-20">
      <UIcon name="i-lucide-book-x" class="size-16 text-warning mx-auto mb-4" />
      <h2 class="text-xl font-semibold mb-2">Нет уроков</h2>
      <p class="text-muted mb-4">
        Сначала создайте хотя бы один урок, чтобы добавить к нему задание
      </p>
      <UButton
        :to="`/teacher/courses/${courseSlug}/lessons/create`"
        color="primary"
        icon="i-lucide-plus"
      >
        Создать урок
      </UButton>
    </div>

    <!-- Form -->
    <template v-else>
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-default">Создание задания</h1>
          <p class="text-muted">Заполните информацию о новом задании</p>
        </div>
        <UButton
          color="neutral"
          variant="ghost"
          icon="i-lucide-arrow-left"
          :to="`/teacher/courses/${courseSlug}/assignments`"
        >
          Назад
        </UButton>
      </div>

      <TeacherAssignmentsForm
        :lessons="lessons"
        :course-slug="courseSlug"
        :is-submitting="isSubmitting"
        :assignment="preselectedLesson ? { lesson: preselectedLesson } as any : null"
        @submit="handleSubmit"
        @cancel="handleCancel"
      />
    </template>
  </div>
</template>
