<script setup lang="ts">
import { z } from "zod";
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

// Fetch assignment
const { data: assignment, status } = await useAsyncData<Assignment>(
  `teacher-assignment-${assignmentId.value}`,
  () => api.get<Assignment>(`/assignments/${assignmentId.value}/`)
);

// Fetch lessons for dropdown
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

// Form state - pre-fill from assignment
const form = reactive<AssignmentForm>({
  lesson: assignment.value?.lesson || "",
  title: assignment.value?.title || "",
  description: assignment.value?.description || "",
  instructions: assignment.value?.instructions || "",
  max_score: assignment.value?.max_score || 100,
  due_date: assignment.value?.due_date
    ? assignment.value.due_date.slice(0, 16)
    : "",
  is_required: assignment.value?.is_required ?? false,
  allow_late_submission: assignment.value?.allow_late_submission ?? true,
});

// Watch for assignment load
watch(
  assignment,
  (newAssignment) => {
    if (newAssignment) {
      form.lesson = newAssignment.lesson;
      form.title = newAssignment.title;
      form.description = newAssignment.description || "";
      form.instructions = newAssignment.instructions || "";
      form.max_score = newAssignment.max_score;
      form.due_date = newAssignment.due_date
        ? newAssignment.due_date.slice(0, 16)
        : "";
      form.is_required = newAssignment.is_required;
      form.allow_late_submission = newAssignment.allow_late_submission;
    }
  },
  { immediate: true }
);

const newFiles = ref<File[]>([]);
const isSubmitting = ref(false);

// Handle new files
const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    newFiles.value = [...newFiles.value, ...Array.from(input.files)];
  }
};

const removeNewFile = (index: number) => {
  newFiles.value.splice(index, 1);
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

// Delete existing file
const deleteExistingFile = async (fileId: number) => {
  try {
    await api.delete(`/assignments/${assignmentId.value}/files/${fileId}/`);
    if (assignment.value) {
      assignment.value.files = assignment.value.files.filter(
        (f) => f.id !== fileId
      );
    }
    toast.add({
      title: "Файл удалён",
      color: "success",
    });
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: "Не удалось удалить файл",
      color: "error",
    });
  }
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

    newFiles.value.forEach((file, index) => {
      formData.append(`files[${index}]`, file);
    });

    await api.fetch(`/assignments/${assignmentId.value}/`, {
      method: "PATCH",
      body: formData,
    });

    toast.add({
      title: "Задание обновлено!",
      color: "success",
    });

    router.push(`/teacher/courses/${courseSlug.value}/assignments`);
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: e.data?.detail || "Не удалось обновить задание",
      color: "error",
    });
  } finally {
    isSubmitting.value = false;
  }
};

// SEO
useHead({
  title: `Редактирование: ${
    assignment.value?.title || "Задание"
  } | Преподаватель`,
});
</script>

<template>
  <div class="max-w-3xl">
    <!-- Header -->
    <div class="mb-8">
      <NuxtLink
        :to="`/teacher/courses/${courseSlug}/assignments`"
        class="inline-flex items-center gap-2 text-sm text-muted hover:text-default transition-colors mb-4"
      >
        <UIcon name="i-lucide-arrow-left" class="size-4" />
        Назад к заданиям
      </NuxtLink>
      <h1 class="text-2xl font-bold text-default">Редактирование задания</h1>
      <p class="text-muted mt-1">{{ assignment?.title }}</p>
    </div>

    <!-- Loading -->
    <div v-if="status === 'pending'" class="space-y-6">
      <USkeleton class="h-40 rounded-xl" />
      <USkeleton class="h-60 rounded-xl" />
      <USkeleton class="h-40 rounded-xl" />
    </div>

    <!-- Form -->
    <form v-else-if="assignment" @submit.prevent="onSubmit" class="space-y-6">
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

      <!-- Existing Files -->
      <div
        v-if="assignment.files && assignment.files.length > 0"
        class="bg-elevated rounded-xl border border-default p-6"
      >
        <h2 class="text-lg font-semibold text-default mb-4">
          Прикреплённые файлы
        </h2>

        <div class="space-y-2">
          <div
            v-for="file in assignment.files"
            :key="file.id"
            class="flex items-center gap-3 px-4 py-3 bg-muted/10 rounded-lg"
          >
            <UIcon name="i-lucide-file" class="size-5 text-muted" />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium truncate">{{ file.filename }}</p>
              <p class="text-xs text-muted">
                {{ formatFileSize(file.file_size) }}
              </p>
            </div>
            <a
              :href="file.file_url"
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
              @click="deleteExistingFile(file.id)"
            />
          </div>
        </div>
      </div>

      <!-- New Files -->
      <div class="bg-elevated rounded-xl border border-default p-6">
        <h2 class="text-lg font-semibold text-default mb-4">Добавить файлы</h2>
        <p class="text-sm text-muted mb-4">
          Добавьте новые материалы к заданию
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

        <!-- New Files List -->
        <div v-if="newFiles.length > 0" class="mt-4 space-y-2">
          <div
            v-for="(file, index) in newFiles"
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

      <!-- Actions -->
      <div class="flex items-center justify-end gap-4 pt-4">
        <UButton
          :to="`/teacher/courses/${courseSlug}/assignments`"
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
      title="Задание не найдено"
      description="Возможно, оно было удалено"
    >
      <template #actions>
        <UButton
          :to="`/teacher/courses/${courseSlug}/assignments`"
          color="primary"
        >
          К списку заданий
        </UButton>
      </template>
    </UEmpty>
  </div>
</template>
