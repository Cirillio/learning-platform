<script setup lang="ts">
import { z } from "zod";
import type { Assignment, Lesson } from "~/types";

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

// Fetch lessons for assignment
interface LessonsResponse {
  count: number;
  results: Lesson[];
}

const { data: lessonsData } = await useAsyncData<LessonsResponse>(
  `teacher-course-lessons-${courseSlug.value}`,
  () => api.get<LessonsResponse>("/lessons/", { course: courseSlug.value })
);

const lessons = computed(() => lessonsData.value?.results || []);

const lessonOptions = computed(() =>
  lessons.value.map((l) => ({
    label: `${l.order}. ${l.title}`,
    value: l.slug,
  }))
);

// Form Schema
const assignmentSchema = z.object({
  lesson: z.string().min(1, "Выберите урок"),
  title: z
    .string()
    .min(3, "Минимум 3 символа")
    .max(200, "Максимум 200 символов"),
  description: z.string().max(1000, "Максимум 1000 символов").optional(),
  instructions: z.string().optional(),
  max_score: z.number().min(1).max(1000),
  due_date: z.string().optional(),
  is_required: z.boolean(),
  allow_late_submission: z.boolean(),
});

type AssignmentForm = z.infer<typeof assignmentSchema>;

// Form state
const form = reactive<AssignmentForm>({
  lesson: "",
  title: "",
  description: "",
  instructions: "",
  max_score: 100,
  due_date: "",
  is_required: false,
  allow_late_submission: true,
});

const attachedFiles = ref<File[]>([]);
const isSubmitting = ref(false);

// Handle files
const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    attachedFiles.value = [...attachedFiles.value, ...Array.from(input.files)];
  }
};

const removeFile = (index: number) => {
  attachedFiles.value.splice(index, 1);
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

// Submit
const onSubmit = async () => {
  const result = assignmentSchema.safeParse(form);
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

    attachedFiles.value.forEach((file, index) => {
      formData.append(`files[${index}]`, file);
    });

    await api.fetch("/assignments/", {
      method: "POST",
      body: formData,
    });

    toast.add({
      title: "Задание создано!",
      color: "success",
    });

    router.push(`/teacher/courses/${courseSlug.value}`);
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: e.data?.detail || "Не удалось создать задание",
      color: "error",
    });
  } finally {
    isSubmitting.value = false;
  }
};

// SEO
useHead({
  title: "Создание задания | Преподаватель",
});
</script>

<template>
  <div class="max-w-3xl">
    <!-- Header -->
    <div class="mb-8">
      <NuxtLink
        :to="`/teacher/courses/${courseSlug}`"
        class="inline-flex items-center gap-2 text-sm text-muted hover:text-default transition-colors mb-4"
      >
        <UIcon name="i-lucide-arrow-left" class="size-4" />
        Назад к курсу
      </NuxtLink>
      <h1 class="text-2xl font-bold text-default">Создание задания</h1>
      <p class="text-muted mt-1">Добавьте новое задание для студентов</p>
    </div>

    <!-- Form -->
    <form @submit.prevent="onSubmit" class="space-y-6">
      <!-- Lesson Selection -->
      <div class="bg-elevated rounded-xl border border-default p-6">
        <h2 class="text-lg font-semibold text-default mb-4">
          Привязка к уроку
        </h2>

        <UFormField label="Урок" required>
          <USelect
            v-model="form.lesson"
            :items="lessonOptions"
            placeholder="Выберите урок"
            class="w-full"
          />
        </UFormField>
      </div>

      <!-- Basic Info -->
      <div class="bg-elevated rounded-xl border border-default p-6">
        <h2 class="text-lg font-semibold text-default mb-4">
          Информация о задании
        </h2>

        <div class="space-y-4">
          <UFormField label="Название задания" required>
            <UInput
              v-model="form.title"
              placeholder="Например: Практическое задание #1"
              class="w-full"
            />
          </UFormField>

          <UFormField label="Краткое описание">
            <UTextarea
              v-model="form.description"
              placeholder="О чём это задание"
              :rows="2"
              class="w-full"
            />
          </UFormField>

          <UFormField
            label="Инструкции"
            hint="Подробные инструкции, поддерживается Markdown"
          >
            <UTextarea
              v-model="form.instructions"
              placeholder="Опишите, что нужно сделать..."
              :rows="6"
              class="w-full"
            />
          </UFormField>
        </div>
      </div>

      <!-- Scoring & Deadline -->
      <div class="bg-elevated rounded-xl border border-default p-6">
        <h2 class="text-lg font-semibold text-default mb-4">
          Оценивание и сроки
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <UFormField label="Максимальный балл" required>
            <UInput
              v-model.number="form.max_score"
              type="number"
              :min="1"
              :max="1000"
              class="w-full"
            />
          </UFormField>

          <UFormField label="Срок сдачи">
            <UInput
              v-model="form.due_date"
              type="datetime-local"
              class="w-full"
            />
          </UFormField>
        </div>

        <div class="flex flex-col gap-3 mt-6">
          <UCheckbox
            v-model="form.is_required"
            label="Обязательное задание"
            description="Студент должен сдать это задание для прохождения курса"
          />

          <UCheckbox
            v-model="form.allow_late_submission"
            label="Разрешить сдачу после срока"
            description="Студенты смогут сдать работу после дедлайна (будет отмечено как просроченное)"
          />
        </div>
      </div>

      <!-- Attached Files -->
      <div class="bg-elevated rounded-xl border border-default p-6">
        <h2 class="text-lg font-semibold text-default mb-4">
          Прикреплённые файлы
        </h2>
        <p class="text-sm text-muted mb-4">
          Добавьте материалы, которые помогут студентам выполнить задание
        </p>

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
          <p class="text-xs text-muted mt-1">PDF, DOC, ZIP до 10MB</p>
        </div>

        <!-- Files List -->
        <div v-if="attachedFiles.length > 0" class="mt-4 space-y-2">
          <div
            v-for="(file, index) in attachedFiles"
            :key="index"
            class="flex items-center gap-3 px-4 py-2 bg-muted/10 rounded-lg"
          >
            <UIcon name="i-lucide-file" class="size-4 text-muted" />
            <span class="flex-1 text-sm truncate">{{ file.name }}</span>
            <span class="text-xs text-muted">{{
              formatFileSize(file.size)
            }}</span>
            <UButton
              color="error"
              variant="ghost"
              size="xs"
              icon="i-lucide-x"
              @click="removeFile(index)"
            />
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-end gap-4 pt-4">
        <UButton
          :to="`/teacher/courses/${courseSlug}`"
          color="neutral"
          variant="ghost"
        >
          Отмена
        </UButton>
        <UButton
          type="submit"
          color="primary"
          :loading="isSubmitting"
          icon="i-lucide-plus"
        >
          Создать задание
        </UButton>
      </div>
    </form>
  </div>
</template>
