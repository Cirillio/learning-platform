<script setup lang="ts">
import { z } from "zod";
import type { Category, Course } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Создание курса",
});

const api = useApi();
const toast = useToast();
const router = useRouter();

// Form Schema
const courseSchema = z.object({
  title: z
    .string()
    .min(3, "Минимум 3 символа")
    .max(200, "Максимум 200 символов"),
  slug: z
    .string()
    .min(3, "Минимум 3 символа")
    .max(200, "Максимум 200 символов")
    .regex(
      /^[a-z0-9-]+$/,
      "Slug может содержать только строчные буквы, цифры и дефисы"
    ),
  short_description: z
    .string()
    .min(10, "Минимум 10 символов")
    .max(500, "Максимум 500 символов"),
  description: z.string().min(50, "Минимум 50 символов"),
  category: z.number({ message: "Выберите категорию" }),
  difficulty: z.enum(["beginner", "intermediate", "advanced"]),
  duration_weeks: z.number().min(1).max(52).nullable(),
  max_students: z.number().min(1).max(1000).nullable(),
  status: z.enum(["draft", "published"]),
  cover_image: z.string().optional(),
});

type CourseForm = z.infer<typeof courseSchema>;

// Form state
const form = reactive<CourseForm>({
  title: "",
  slug: "",
  short_description: "",
  description: "",
  category: 0,
  difficulty: "beginner",
  duration_weeks: null,
  max_students: null,
  status: "draft",
  cover_image: "",
});

const coverPreview = ref<string | null>(null);
const isSubmitting = ref(false);

// Generate slug from title
watch(
  () => form.title,
  (newTitle) => {
    if (newTitle) {
      form.slug = newTitle
        .toLowerCase()
        .replace(/[^a-zа-яё0-9\s-]/g, "") // Remove special chars except spaces and hyphens
        .replace(/\s+/g, "-") // Replace spaces with hyphens
        .replace(/-+/g, "-") // Replace multiple hyphens with single
        .replace(/^-|-$/g, ""); // Remove leading/trailing hyphens
    }
  }
);

// Initialize cover preview from existing image
watch(
  () => form.cover_image,
  (url) => {
    coverPreview.value = url || null;
  },
  { immediate: true }
);

// Fetch categories
interface CategoriesResponse {
  count: number;
  results: Category[];
}

const { data: categoriesData } = await useAsyncData<CategoriesResponse>(
  "categories",
  () => api.get<CategoriesResponse>("/categories/")
);

const categories = computed(() => categoriesData.value?.results || []);

const categoryOptions = computed(() =>
  categories.value.map((c) => ({
    label: c.name,
    value: c.id,
  }))
);

const difficultyOptions = [
  { label: "Начальный", value: "beginner" },
  { label: "Средний", value: "intermediate" },
  { label: "Продвинутый", value: "advanced" },
];

const statusOptions = [
  { label: "Черновик", value: "draft" },
  { label: "Опубликован", value: "published" },
];

// Submit
const onSubmit = async () => {
  const result = courseSchema.safeParse(form);
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
    const response = await api.post<Course>("/courses/", form);

    toast.add({
      title: "Курс создан!",
      description: "Теперь добавьте уроки и материалы",
      color: "success",
    });

    console.log("Created course:", response.slug);

    navigateTo(`/teacher/courses/${response.slug}`);
  } catch (e: any) {
    // Handle validation errors from server
    if (e.status === 400 && e.data) {
      const errors = Object.entries(e.data)
        .map(
          ([field, messages]) =>
            `${field}: ${
              Array.isArray(messages) ? messages.join(", ") : messages
            }`
        )
        .join("; ");
      toast.add({
        title: "Ошибка валидации",
        description: errors || "Проверьте введённые данные",
        color: "error",
      });
    } else {
      toast.add({
        title: "Ошибка",
        description: e.data?.detail || "Не удалось создать курс",
        color: "error",
      });
    }
  } finally {
    isSubmitting.value = false;
  }
};

// SEO
useHead({
  title: "Создание курса | Преподаватель",
});
</script>

<template>
  <div class="">
    <!-- Header -->
    <div class="mb-2">
      <NuxtLink
        to="/teacher/courses"
        class="inline-flex items-center gap-2 text-sm text-muted hover:text-default transition-colors"
      >
        <UIcon name="i-lucide-arrow-left" class="size-4" />
        Назад к курсам
      </NuxtLink>
      <h1 class="text-4xl font-bold text-default">Создание нового курса</h1>
      <p class="text-muted text-lg mt-1">Заполните информацию о курсе</p>
    </div>

    <!-- Form -->
    <form @submit.prevent="onSubmit" class="flex flex-col gap-2">
      <div class="flex gap-2">
        <!-- Basic Info -->
        <UCard class="flex-1/2">
          <template #header>
            <h2 class="text-2xl font-semibold text-default">
              Основная информация
            </h2>
          </template>

          <div class="space-y-6">
            <UFormField size="xl" label="Название курса" required>
              <UInput
                v-model="form.title"
                placeholder="Например: Основы веб-разработки"
                class="w-full"
              />
            </UFormField>

            <UFormField
              size="xl"
              label="Slug"
              required
              hint="URL-идентификатор курса"
            >
              <UInput
                v-model="form.slug"
                placeholder="osnovy-veb-razrabotki"
                class="w-full"
              />
            </UFormField>

            <UFormField
              size="xl"
              label="Краткое описание"
              required
              hint="Будет показано в карточке курса"
            >
              <UTextarea
                v-model="form.short_description"
                placeholder="Краткое описание курса в 1-2 предложения"
                :rows="2"
                class="w-full"
              />
            </UFormField>

            <UFormField
              size="xl"
              label="Полное описание"
              required
              hint="Поддерживается Markdown"
            >
              <UTextarea
                v-model="form.description"
                placeholder="Подробное описание курса..."
                :rows="8"
                class="w-full"
              />
            </UFormField>
          </div>
        </UCard>

        <div class="flex flex-1/2 h-fit flex-col gap-2">
          <!-- Cover Image -->
          <UCard class="">
            <template #header>
              <h2 class="text-2xl font-semibold text-default">Обложка курса</h2>
            </template>

            <UFormField label="URL обложки" hint="Ссылка на изображение">
              <UInput
                v-model="form.cover_image"
                placeholder="https://example.com/image.jpg"
                class="w-full"
              />
            </UFormField>

            <div v-if="coverPreview" class="mt-4">
              <img
                :src="coverPreview"
                alt="Cover preview"
                class="w-full aspect-video object-cover rounded-xl"
              />
            </div>
          </UCard>

          <!-- Settings -->
          <UCard class="flex-2/3 h-fit">
            <template #header>
              <h2 class="text-2xl font-semibold text-default">Настройки</h2>
            </template>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <UFormField size="xl" label="Категория" required>
                <USelect
                  v-model="form.category"
                  :items="categoryOptions"
                  placeholder="Выберите категорию"
                  class="w-full"
                />
              </UFormField>

              <UFormField size="xl" label="Уровень сложности" required>
                <USelect
                  v-model="form.difficulty"
                  :items="difficultyOptions"
                  class="w-full"
                />
              </UFormField>

              <UFormField size="xl" label="Длительность (недель)">
                <UInput
                  v-model.number="form.duration_weeks"
                  type="number"
                  :min="1"
                  :max="52"
                  placeholder="Например: 8"
                  class="w-full"
                />
              </UFormField>

              <UFormField size="xl" label="Максимум студентов">
                <UInput
                  v-model.number="form.max_students"
                  type="number"
                  :min="1"
                  :max="1000"
                  placeholder="Например: 100"
                  class="w-full"
                />
              </UFormField>
            </div>
          </UCard>

          <!-- Status -->
          <UCard class="flex-1/3 h-fit">
            <h2 class="text-lg font-semibold text-default mb-6">
              Статус публикации
            </h2>

            <UFormField size="xl" label="Статус">
              <URadioGroup
                v-model="form.status"
                :items="statusOptions"
                class="flex gap-4"
                :ui="{
                  label: 'cursor-pointer',
                  base: 'cursor-pointer',
                }"
              />
            </UFormField>
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
            icon="i-lucide-plus"
            size="xl"
          >
            Создать курс
          </UButton>
          <UButton
            to="/teacher/courses"
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
