<script setup lang="ts">
import { z } from "zod";
import type { Category } from "~/types";

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
});

type CourseForm = z.infer<typeof courseSchema>;

// Form state
const form = reactive<CourseForm>({
  title: "",
  short_description: "",
  description: "",
  category: 0,
  difficulty: "beginner",
  duration_weeks: null,
  max_students: null,
  status: "draft",
});

const coverImage = ref<File | null>(null);
const coverPreview = ref<string | null>(null);
const isSubmitting = ref(false);

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
  { label: "Опубликовать", value: "published" },
];

// Handle cover image
const onCoverChange = (file: File) => {
  coverImage.value = file;
  coverPreview.value = URL.createObjectURL(file);
};

const removeCover = () => {
  coverImage.value = null;
  coverPreview.value = null;
};

// Submit
const onSubmit = async () => {
  // Validate
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
    const formData = new FormData();
    Object.entries(form).forEach(([key, value]) => {
      if (value !== null && value !== undefined) {
        formData.append(key, String(value));
      }
    });

    if (coverImage.value) {
      formData.append("cover_image", coverImage.value);
    }

    const response = await api.fetch<{ slug: string }>("/courses/", {
      method: "POST",
      body: formData,
    });

    toast.add({
      title: "Курс создан!",
      description: "Теперь добавьте уроки и материалы",
      color: "success",
    });

    router.push(`/teacher/courses/${response.slug}`);
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: e.data?.detail || "Не удалось создать курс",
      color: "error",
    });
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
  <div class="max-w-4xl">
    <!-- Header -->
    <div class="mb-8">
      <NuxtLink
        to="/teacher/courses"
        class="inline-flex items-center gap-2 text-sm text-muted hover:text-default transition-colors mb-4"
      >
        <UIcon name="i-lucide-arrow-left" class="size-4" />
        Назад к курсам
      </NuxtLink>
      <h1 class="text-2xl font-bold text-default">Создание нового курса</h1>
      <p class="text-muted mt-1">Заполните информацию о курсе</p>
    </div>

    <!-- Form -->
    <form @submit.prevent="onSubmit" class="space-y-8">
      <!-- Basic Info -->
      <TeacherCourseFormBasicInfo :form="form" />

      <!-- Cover Image -->
      <TeacherCourseFormCoverImage
        :preview="coverPreview"
        @change="onCoverChange"
        @remove="removeCover"
      />

      <!-- Settings -->
      <TeacherCourseFormSettings
        :form="form"
        :category-options="categoryOptions"
        :difficulty-options="difficultyOptions"
      />

      <!-- Publish Settings -->
      <TeacherCourseFormPublishSettings
        :form="form"
        :status-options="statusOptions"
      />

      <!-- Actions -->
      <div class="flex items-center justify-end gap-4 pt-4">
        <UButton to="/teacher/courses" color="neutral" variant="ghost">
          Отмена
        </UButton>
        <UButton
          type="submit"
          color="primary"
          :loading="isSubmitting"
          icon="i-lucide-plus"
        >
          Создать курс
        </UButton>
      </div>
    </form>
  </div>
</template>
