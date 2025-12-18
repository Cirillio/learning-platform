<script setup lang="ts">
definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Создание урока",
});

const route = useRoute();
const router = useRouter();
const api = useApi();
const toast = useToast();

const courseSlug = computed(() => route.params.slug as string);
const isSubmitting = ref(false);

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
    const newLesson = await api.post<{ slug: string }>("/lessons/", {
      ...formData,
      course: courseSlug.value,
    });
    toast.add({
      title: "Урок создан",
      description: "Новый урок успешно добавлен",
      color: "success",
    });
    router.push(
      `/teacher/courses/${courseSlug.value}/lessons/${newLesson.slug}`
    );
  } catch (error) {
    toast.add({
      title: "Ошибка",
      description: (error as Error).message || "Не удалось создать урок",
      color: "error",
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Cancel handler
const handleCancel = () => {
  router.push(`/teacher/courses/${courseSlug.value}/lessons`);
};
</script>

<template>
  <div class="mx-auto max-w-3xl space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-default">Создание урока</h1>
        <p class="text-muted">Заполните информацию о новом уроке</p>
      </div>
      <UButton
        color="neutral"
        variant="ghost"
        icon="i-lucide-arrow-left"
        :to="`/teacher/courses/${courseSlug}/lessons`"
      >
        Назад
      </UButton>
    </div>

    <TeacherLessonsForm
      :course-slug="courseSlug"
      :is-submitting="isSubmitting"
      @submit="handleSubmit"
      @cancel="handleCancel"
    />
  </div>
</template>
