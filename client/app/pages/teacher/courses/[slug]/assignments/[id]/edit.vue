<script setup lang="ts">
import type { Assignment, Lesson } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Редактирование задания",
});

const route = useRoute();
const router = useRouter();
const api = useApi();
const toast = useToast();

const courseSlug = computed(() => route.params.slug as string);
const assignmentId = computed(() => route.params.id as string);

const isSubmitting = ref(false);

// Fetch assignment data
const { data: assignment, status: assignmentStatus } =
  await useAsyncData<Assignment>(
    `teacher-edit-assignment-${assignmentId.value}`,
    () => api.get<Assignment>(`/assignments/${assignmentId.value}/`)
  );

// Fetch lessons for dropdown
interface LessonsResponse {
  count: number;
  results: Lesson[];
}

const { data: lessonsData, status: lessonsStatus } =
  await useAsyncData<LessonsResponse>(
    `teacher-course-lessons-${courseSlug.value}`,
    () => api.get<LessonsResponse>("/lessons/", { course: courseSlug.value })
  );

const lessons = computed(() => lessonsData.value?.results || []);

// Combined loading status
const isLoading = computed(
  () =>
    assignmentStatus.value === "pending" || lessonsStatus.value === "pending"
);

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
    await api.patch(`/assignments/${assignmentId.value}/`, formData);
    toast.add({
      title: "Задание обновлено",
      description: "Изменения успешно сохранены",
      color: "success",
    });
    router.push(
      `/teacher/courses/${courseSlug.value}/assignments/${assignmentId.value}`
    );
  } catch (error) {
    toast.add({
      title: "Ошибка",
      description: (error as Error).message || "Не удалось сохранить изменения",
      color: "error",
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Cancel handler
const handleCancel = () => {
  router.push(
    `/teacher/courses/${courseSlug.value}/assignments/${assignmentId.value}`
  );
};
</script>

<template>
  <div class="mx-auto max-w-3xl space-y-6">
    <!-- Loading -->
    <div v-if="isLoading" class="space-y-6">
      <USkeleton class="h-12 w-64 rounded-lg" />
      <USkeleton class="h-6 w-48 rounded-lg" />
      <USkeleton class="h-[500px] rounded-xl" />
    </div>

    <!-- Error: Assignment not found -->
    <div v-else-if="!assignment" class="text-center py-20">
      <UIcon
        name="i-lucide-alert-circle"
        class="size-16 text-error mx-auto mb-4"
      />
      <h2 class="text-xl font-semibold mb-2">Задание не найдено</h2>
      <p class="text-muted mb-4">
        Задание с указанным идентификатором не существует или было удалено
      </p>
      <UButton
        :to="`/teacher/courses/${courseSlug}/assignments`"
        color="primary"
      >
        К списку заданий
      </UButton>
    </div>

    <!-- Form -->
    <template v-else>
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-default">
            Редактирование задания
          </h1>
          <p class="text-muted">
            Измените информацию о задании "{{ assignment.title }}"
          </p>
        </div>
        <UButton
          color="neutral"
          variant="ghost"
          icon="i-lucide-arrow-left"
          :to="`/teacher/courses/${courseSlug}/assignments/${assignmentId}`"
        >
          Назад
        </UButton>
      </div>

      <TeacherAssignmentsForm
        :assignment="assignment"
        :lessons="lessons"
        :course-slug="courseSlug"
        :is-submitting="isSubmitting"
        @submit="handleSubmit"
        @cancel="handleCancel"
      />
    </template>
  </div>
</template>
