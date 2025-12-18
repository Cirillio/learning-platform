<script setup lang="ts">
import type { LessonDetail } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Редактирование урока",
});

const route = useRoute();
const router = useRouter();
const api = useApi();
const toast = useToast();

const courseSlug = computed(() => route.params.slug as string);
const lessonSlug = computed(() => route.params.lesson_slug as string);

const isSubmitting = ref(false);

// Fetch lesson data
const { data: lesson, status } = await useAsyncData<LessonDetail>(
  `teacher-edit-lesson-${lessonSlug.value}`,
  () => api.get<LessonDetail>(`/lessons/${lessonSlug.value}/`)
);

// Form submit handler
const handleSubmit = async (formData: {
  title: string;
  description?: string;
  content?: string;
  video_url?: string;
  duration_minutes: number;
  is_published: boolean;
}) => {
  isSubmitting.value = true;
  try {
    await api.patch(`/lessons/${lessonSlug.value}/`, formData);
    toast.add({
      title: "Урок обновлен",
      description: "Изменения успешно сохранены",
      color: "success",
    });
    router.push(
      `/teacher/courses/${courseSlug.value}/lessons/${lessonSlug.value}`
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
    `/teacher/courses/${courseSlug.value}/lessons/${lessonSlug.value}`
  );
};
</script>

<template>
  <div class="mx-auto max-w-3xl space-y-6">
    <!-- Loading -->
    <div v-if="status === 'pending'" class="space-y-6">
      <USkeleton class="h-12 w-64 rounded-lg" />
      <USkeleton class="h-6 w-48 rounded-lg" />
      <USkeleton class="h-[400px] rounded-xl" />
    </div>

    <!-- Error -->
    <div v-else-if="!lesson" class="text-center py-20">
      <UIcon
        name="i-lucide-alert-circle"
        class="size-16 text-error mx-auto mb-4"
      />
      <h2 class="text-xl font-semibold mb-2">Урок не найден</h2>
      <p class="text-muted mb-4">
        Урок с указанным идентификатором не существует или был удален
      </p>
      <UButton :to="`/teacher/courses/${courseSlug}/lessons`" color="primary">
        К списку уроков
      </UButton>
    </div>

    <!-- Form -->
    <template v-else>
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-default">Редактирование урока</h1>
          <p class="text-muted">
            Измените информацию об уроке "{{ lesson.title }}"
          </p>
        </div>
        <UButton
          color="neutral"
          variant="ghost"
          icon="i-lucide-arrow-left"
          :to="`/teacher/courses/${courseSlug}/lessons/${lessonSlug}`"
        >
          Назад
        </UButton>
      </div>

      <TeacherLessonsForm
        :lesson="lesson"
        :course-slug="courseSlug"
        :is-submitting="isSubmitting"
        @submit="handleSubmit"
        @cancel="handleCancel"
      />
    </template>
  </div>
</template>
