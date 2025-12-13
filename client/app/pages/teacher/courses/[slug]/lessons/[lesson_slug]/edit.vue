<script setup lang="ts">
import { z } from "zod";
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

// Fetch lesson
const { data: lesson, status } = await useAsyncData<LessonDetail>(
  `teacher-lesson-${lessonSlug.value}`,
  () => api.get<LessonDetail>(`/lessons/${lessonSlug.value}/`)
);

// Form schema
const lessonSchema = z.object({
  title: z
    .string()
    .min(3, "Минимум 3 символа")
    .max(200, "Максимум 200 символов"),
  description: z.string().max(500, "Максимум 500 символов").optional(),
  content: z.string().optional(),
  video_url: z
    .string()
    .url("Введите корректный URL")
    .optional()
    .or(z.literal("")),
  duration_minutes: z.number().min(0).max(600).optional(),
  is_published: z.boolean(),
});

type LessonForm = z.infer<typeof lessonSchema>;

// Form state - pre-fill from lesson
const form = reactive<LessonForm>({
  title: lesson.value?.title || "",
  description: lesson.value?.description || "",
  content: lesson.value?.content || "",
  video_url: lesson.value?.video_url || "",
  duration_minutes: lesson.value?.duration_minutes || 0,
  is_published: lesson.value?.is_published ?? false,
});

// Watch for lesson load
watch(
  lesson,
  (newLesson) => {
    if (newLesson) {
      form.title = newLesson.title;
      form.description = newLesson.description || "";
      form.content = newLesson.content || "";
      form.video_url = newLesson.video_url || "";
      form.duration_minutes = newLesson.duration_minutes || 0;
      form.is_published = newLesson.is_published;
    }
  },
  { immediate: true }
);

const newMaterials = ref<File[]>([]);
const isSubmitting = ref(false);

// Handle new files
const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    newMaterials.value = [...newMaterials.value, ...Array.from(input.files)];
  }
};

const removeNewFile = (index: number) => {
  newMaterials.value.splice(index, 1);
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

// Delete existing material
const deleteExistingMaterial = async (materialId: number) => {
  try {
    await api.delete(`/lessons/${lessonSlug.value}/materials/${materialId}/`);
    if (lesson.value) {
      lesson.value.materials = lesson.value.materials.filter(
        (m) => m.id !== materialId
      );
    }
    toast.add({
      title: "Материал удалён",
      color: "success",
    });
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: "Не удалось удалить материал",
      color: "error",
    });
  }
};

// Submit
const onSubmit = async () => {
  const result = lessonSchema.safeParse(form);
  if (!result.success) {
    const firstIssue = result.error.issues[0];
    toast.add({
      title: "Ошибка валидации",
      description: firstIssue?.message || "Проверьте введённые данные",
      color: "error",
    });
    return;
  }

  isSubmitting.value = true;

  try {
    const formData = new FormData();
    Object.entries(form).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== "") {
        formData.append(key, String(value));
      }
    });

    newMaterials.value.forEach((file, index) => {
      formData.append(`materials[${index}]`, file);
    });

    await api.fetch(`/lessons/${lessonSlug.value}/`, {
      method: "PATCH",
      body: formData,
    });

    toast.add({
      title: "Урок обновлён!",
      color: "success",
    });

    router.push(`/teacher/courses/${courseSlug.value}/lessons`);
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: e.data?.detail || "Не удалось обновить урок",
      color: "error",
    });
  } finally {
    isSubmitting.value = false;
  }
};

// SEO
useHead({
  title: `Редактирование: ${lesson.value?.title || "Урок"} | Преподаватель`,
});
</script>

<template>
  <div class="max-w-3xl">
    <!-- Header -->
    <div class="mb-8">
      <NuxtLink
        :to="`/teacher/courses/${courseSlug}/lessons`"
        class="inline-flex items-center gap-2 text-sm text-muted hover:text-default transition-colors mb-4"
      >
        <UIcon name="i-lucide-arrow-left" class="size-4" />
        Назад к урокам
      </NuxtLink>
      <h1 class="text-2xl font-bold text-default">Редактирование урока</h1>
      <p class="text-muted mt-1">{{ lesson?.title }}</p>
    </div>

    <!-- Loading -->
    <div v-if="status === 'pending'" class="space-y-6">
      <USkeleton class="h-40 rounded-xl" />
      <USkeleton class="h-32 rounded-xl" />
      <USkeleton class="h-64 rounded-xl" />
    </div>

    <!-- Form -->
    <form v-else-if="lesson" @submit.prevent="onSubmit" class="space-y-6">
      <!-- Basic Info -->
      <div class="bg-elevated rounded-xl border border-default p-6">
        <h2 class="text-lg font-semibold text-default mb-4">
          Основная информация
        </h2>

        <div class="space-y-4">
          <UFormField label="Название урока" required>
            <UInput
              v-model="form.title"
              placeholder="Введение в тему"
              class="w-full"
            />
          </UFormField>

          <UFormField label="Краткое описание">
            <UTextarea
              v-model="form.description"
              placeholder="О чём этот урок"
              :rows="2"
              class="w-full"
            />
          </UFormField>
        </div>
      </div>

      <!-- Video -->
      <div class="bg-elevated rounded-xl border border-default p-6">
        <h2 class="text-lg font-semibold text-default mb-4">Видео</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <UFormField
            label="URL видео"
            hint="YouTube, Vimeo, или прямая ссылка"
          >
            <UInput
              v-model="form.video_url"
              placeholder="https://youtube.com/watch?v=..."
              class="w-full"
            />
          </UFormField>

          <UFormField label="Длительность (мин.)">
            <UInput
              v-model.number="form.duration_minutes"
              type="number"
              :min="0"
              :max="600"
              class="w-full"
            />
          </UFormField>
        </div>
      </div>

      <!-- Content -->
      <div class="bg-elevated rounded-xl border border-default p-6">
        <h2 class="text-lg font-semibold text-default mb-4">
          Текстовый контент
        </h2>
        <p class="text-sm text-muted mb-4">
          Поддерживается Markdown форматирование
        </p>

        <UTextarea
          v-model="form.content"
          placeholder="# Заголовок урока..."
          :rows="12"
          class="w-full font-mono text-sm"
        />
      </div>

      <!-- Existing Materials -->
      <div
        v-if="lesson.materials && lesson.materials.length > 0"
        class="bg-elevated rounded-xl border border-default p-6"
      >
        <h2 class="text-lg font-semibold text-default mb-4">
          Текущие материалы
        </h2>

        <div class="space-y-2">
          <div
            v-for="material in lesson.materials"
            :key="material.id"
            class="flex items-center gap-3 px-4 py-3 bg-muted/10 rounded-lg"
          >
            <UIcon name="i-lucide-file" class="size-5 text-muted" />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium truncate">{{ material.title }}</p>
              <p class="text-xs text-muted">
                {{ formatFileSize(material.file_size) }}
              </p>
            </div>
            <a
              :href="material.file_url"
              target="_blank"
              class="text-primary hover:underline text-sm"
            >
              Скачать
            </a>
            <UButton
              color="error"
              variant="ghost"
              size="xs"
              icon="i-lucide-trash-2"
              @click="deleteExistingMaterial(material.id)"
            />
          </div>
        </div>
      </div>

      <!-- New Materials -->
      <div class="bg-elevated rounded-xl border border-default p-6">
        <h2 class="text-lg font-semibold text-default mb-4">
          Добавить материалы
        </h2>
        <p class="text-sm text-muted mb-4">Прикрепите новые файлы к уроку</p>

        <div
          class="border-2 border-dashed border-default rounded-xl p-8 text-center hover:border-primary/50 transition-colors cursor-pointer"
          @click="($refs.fileInput as HTMLInputElement).click()"
        >
          <input
            ref="fileInput"
            type="file"
            multiple
            class="hidden"
            @change="handleFileChange"
          />
          <UIcon
            name="i-lucide-upload-cloud"
            class="size-10 text-muted mx-auto mb-3"
          />
          <p class="text-muted">Нажмите для загрузки или перетащите файлы</p>
          <p class="text-xs text-muted mt-1">PDF, DOC, PPT, ZIP до 50MB</p>
        </div>

        <!-- New Files List -->
        <div v-if="newMaterials.length > 0" class="mt-4 space-y-2">
          <div
            v-for="(file, index) in newMaterials"
            :key="index"
            class="flex items-center gap-3 px-4 py-2 bg-success/10 rounded-lg border border-success/20"
          >
            <UIcon name="i-lucide-file-plus" class="size-4 text-success" />
            <span class="flex-1 text-sm truncate">{{ file.name }}</span>
            <span class="text-xs text-muted">{{
              formatFileSize(file.size)
            }}</span>
            <UBadge color="success" variant="subtle" size="xs">Новый</UBadge>
            <UButton
              color="error"
              variant="ghost"
              size="xs"
              icon="i-lucide-x"
              @click="removeNewFile(index)"
            />
          </div>
        </div>
      </div>

      <!-- Publishing -->
      <div class="bg-elevated rounded-xl border border-default p-6">
        <h2 class="text-lg font-semibold text-default mb-4">Публикация</h2>

        <UCheckbox
          v-model="form.is_published"
          label="Опубликовать урок"
          description="Урок будет доступен студентам. Иначе сохранится как черновик."
        />
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-end gap-4 pt-4">
        <UButton
          :to="`/teacher/courses/${courseSlug}/lessons`"
          color="neutral"
          variant="ghost"
        >
          Отмена
        </UButton>
        <UButton
          type="submit"
          color="primary"
          :loading="isSubmitting"
          icon="i-lucide-save"
        >
          Сохранить изменения
        </UButton>
      </div>
    </form>

    <!-- Not Found -->
    <UEmpty
      v-else
      icon="i-lucide-file-question"
      title="Урок не найден"
      description="Возможно, он был удалён"
    >
      <template #actions>
        <UButton :to="`/teacher/courses/${courseSlug}/lessons`" color="primary">
          К списку уроков
        </UButton>
      </template>
    </UEmpty>
  </div>
</template>
