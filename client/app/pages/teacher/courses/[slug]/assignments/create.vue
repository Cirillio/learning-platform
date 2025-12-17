<script setup lang="ts">
import { z } from "zod";
import type { Lesson } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Создание задания",
});

const route = useRoute();
const router = useRouter();
const toast = useToast();
const assignmentsService = useAssignmentsService();
const lessonsService = useLessonsService();

const courseSlug = computed(() => route.params.slug as string);
// const selectedLessonSlug = computed(() => route.query.lesson as string);

// Fetch lessons for assignment
interface LessonsResponse {
  count: number;
  results: Lesson[];
}

const { data: lessonsData } = await useAsyncData<LessonsResponse>(
  `teacher-course-lessons-${courseSlug.value}`,
  () => lessonsService.getLessonsByCourse(courseSlug.value)
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
  max_score: z
    .number()
    .min(1, "Минимум 1 балл")
    .max(1000, "Максимум 1000 баллов"),
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
const fileInputRef = ref<HTMLInputElement | null>(null);

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

const getFileIcon = (filename: string): string => {
  const ext = filename.split(".").pop()?.toLowerCase();
  const icons: Record<string, string> = {
    pdf: "i-lucide-file-text",
    doc: "i-lucide-file-text",
    docx: "i-lucide-file-text",
    zip: "i-lucide-file-archive",
    rar: "i-lucide-file-archive",
    png: "i-lucide-image",
    jpg: "i-lucide-image",
    jpeg: "i-lucide-image",
  };
  return icons[ext || ""] || "i-lucide-file";
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
    await assignmentsService.createAssignment({
      lesson: form.lesson,
      title: form.title,
      description: form.description || undefined,
      instructions: form.instructions || undefined,
      max_score: form.max_score,
      due_date: form.due_date || null,
      is_required: form.is_required,
      allow_late_submission: form.allow_late_submission,
    });

    toast.add({
      title: "Задание создано!",
      description: "Задание успешно добавлено к уроку",
      color: "success",
    });

    router.push(`/teacher/courses/${courseSlug.value}`);
  } catch (e: unknown) {
    const error = e as { data?: { detail?: string; [key: string]: unknown } };

    if (error.data && typeof error.data === "object") {
      const errors = Object.entries(error.data)
        .filter(([key]) => key !== "detail")
        .map(
          ([field, messages]) =>
            `${field}: ${
              Array.isArray(messages) ? messages.join(", ") : messages
            }`
        )
        .join("; ");

      if (errors) {
        toast.add({
          title: "Ошибка валидации",
          description: errors,
          color: "error",
        });
        return;
      }
    }

    toast.add({
      title: "Ошибка",
      description:
        (error.data?.detail as string) || "Не удалось создать задание",
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
  <div class="">
    <!-- Header -->
    <div class="mb-2">
      <NuxtLink
        :to="`/teacher/courses/${courseSlug}`"
        class="inline-flex items-center gap-2 text-sm text-muted hover:text-default transition-colors"
      >
        <UIcon name="i-lucide-arrow-left" class="size-4" />
        Назад к курсу
      </NuxtLink>
      <h1 class="text-4xl font-bold text-default">Создание нового задания</h1>
      <p class="text-muted text-lg mt-1">
        Добавьте задание для проверки знаний студентов
      </p>
    </div>

    <!-- Form -->
    <form @submit.prevent="onSubmit" class="flex flex-col gap-2">
      <div class="flex gap-2">
        <!-- Left Column: Main Info -->
        <div class="flex-1/2 flex flex-col gap-2">
          <!-- Lesson Selection -->
          <UCard>
            <template #header>
              <h2 class="text-2xl font-semibold text-default">
                Привязка к уроку
              </h2>
            </template>

            <UFormField
              size="xl"
              label="Урок"
              required
              hint="Выберите урок, к которому относится задание"
            >
              <USelect
                v-model="form.lesson"
                :items="lessonOptions"
                placeholder="Выберите урок"
                class="w-full"
                size="lg"
              />
            </UFormField>

            <p v-if="lessons.length === 0" class="text-warning text-base mt-3">
              <UIcon name="i-lucide-alert-triangle" class="size-4 mr-1" />
              Сначала создайте хотя бы один урок в курсе
            </p>
          </UCard>

          <!-- Basic Info -->
          <UCard>
            <template #header>
              <h2 class="text-2xl font-semibold text-default">
                Информация о задании
              </h2>
            </template>

            <div class="space-y-6">
              <UFormField size="xl" label="Название задания" required>
                <UInput
                  v-model="form.title"
                  placeholder="Например: Практическое задание #1"
                  class="w-full"
                  size="lg"
                />
              </UFormField>

              <UFormField
                size="xl"
                label="Краткое описание"
                hint="Краткое описание задания для списка"
              >
                <UTextarea
                  v-model="form.description"
                  placeholder="О чём это задание..."
                  :rows="2"
                  class="w-full"
                  size="lg"
                />
              </UFormField>

              <UFormField
                size="xl"
                label="Инструкции"
                hint="Подробные инструкции, поддерживается Markdown"
              >
                <UTextarea
                  v-model="form.instructions"
                  placeholder="Опишите, что нужно сделать студенту..."
                  :rows="8"
                  class="w-full"
                  size="lg"
                />
              </UFormField>
            </div>
          </UCard>
        </div>

        <!-- Right Column: Settings & Files -->
        <div class="flex-1/2 flex flex-col gap-2">
          <!-- Scoring & Deadline -->
          <UCard>
            <template #header>
              <h2 class="text-2xl font-semibold text-default">
                Оценивание и сроки
              </h2>
            </template>

            <div class="grid grid-cols-2 gap-6">
              <UFormField size="xl" label="Максимальный балл" required>
                <UInput
                  v-model.number="form.max_score"
                  type="number"
                  :min="1"
                  :max="1000"
                  class="w-full"
                  size="lg"
                />
              </UFormField>

              <UFormField size="xl" label="Срок сдачи" hint="Опционально">
                <UInput
                  v-model="form.due_date"
                  type="datetime-local"
                  class="w-full"
                  size="lg"
                />
              </UFormField>
            </div>
          </UCard>

          <!-- Requirements -->
          <UCard>
            <template #header>
              <h2 class="text-2xl font-semibold text-default">Требования</h2>
            </template>

            <div class="space-y-4">
              <UCheckbox
                v-model="form.is_required"
                label="Обязательное задание"
              >
                <template #description>
                  <span class="text-base text-muted">
                    Студент должен сдать это задание для прохождения курса
                  </span>
                </template>
              </UCheckbox>

              <UCheckbox
                v-model="form.allow_late_submission"
                label="Разрешить сдачу после срока"
              >
                <template #description>
                  <span class="text-base text-muted">
                    Студенты смогут сдать работу после дедлайна (будет отмечено
                    как просроченное)
                  </span>
                </template>
              </UCheckbox>
            </div>
          </UCard>

          <!-- Attached Files -->
          <UCard>
            <template #header>
              <h2 class="text-2xl font-semibold text-default">
                Прикреплённые файлы
              </h2>
            </template>

            <p class="text-base text-muted mb-4">
              Добавьте материалы, которые помогут студентам выполнить задание
            </p>

            <div
              class="border-2 border-dashed border-default rounded-xl p-8 text-center hover:border-primary/50 hover:bg-primary/5 transition-all cursor-pointer"
              @click="fileInputRef?.click()"
            >
              <input
                ref="fileInputRef"
                type="file"
                multiple
                class="hidden"
                accept=".pdf,.doc,.docx,.zip,.rar,.png,.jpg,.jpeg"
                @change="handleFileChange"
              />
              <UIcon
                name="i-lucide-upload-cloud"
                class="size-12 text-muted mx-auto mb-3"
              />
              <p class="text-base text-default font-medium">
                Нажмите для загрузки или перетащите файлы
              </p>
              <p class="text-sm text-muted mt-1">PDF, DOC, ZIP до 10MB</p>
            </div>

            <!-- Files List -->
            <div v-if="attachedFiles.length > 0" class="mt-4 space-y-2">
              <div
                v-for="(file, index) in attachedFiles"
                :key="index"
                class="flex items-center gap-3 px-4 py-3 bg-muted/10 rounded-xl"
              >
                <UIcon
                  :name="getFileIcon(file.name)"
                  class="size-5 text-muted"
                />
                <span class="flex-1 text-base truncate">{{ file.name }}</span>
                <span class="text-sm text-muted">{{
                  formatFileSize(file.size)
                }}</span>
                <UButton
                  color="error"
                  variant="ghost"
                  size="sm"
                  icon="i-lucide-x"
                  @click.stop="removeFile(index)"
                />
              </div>
            </div>
          </UCard>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <UButton
            type="submit"
            color="primary"
            :loading="isSubmitting"
            :disabled="lessons.length === 0"
            icon="i-lucide-plus"
            size="xl"
          >
            Создать задание
          </UButton>
          <UButton
            :to="`/teacher/courses/${courseSlug}`"
            color="neutral"
            variant="ghost"
            size="xl"
          >
            Отмена
          </UButton>
        </div>
      </div>
    </form>
  </div>
</template>
