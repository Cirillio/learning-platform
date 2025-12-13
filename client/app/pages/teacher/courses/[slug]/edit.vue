<script setup lang="ts">
import { z } from "zod";
import type { CourseDetail, Category } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Редактирование курса",
});

const route = useRoute();
const router = useRouter();
const api = useApi();
const toast = useToast();

const slug = computed(() => route.params.slug as string);

// Fetch course
const { data: course, pending: coursePending } =
  await useAsyncData<CourseDetail>(`teacher-edit-course-${slug.value}`, () =>
    api.get<CourseDetail>(`/courses/${slug.value}/`)
  );

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
  status: z.enum(["draft", "published", "archived"]),
});

type CourseForm = z.infer<typeof courseSchema>;

// Form state - initialize from course data
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

// Watch course data and populate form
watch(
  course,
  (c) => {
    if (c) {
      form.title = c.title;
      form.short_description = c.short_description;
      form.description = c.description;
      form.category =
        typeof c.category === "object" ? c.category.id : c.category;
      form.difficulty = c.difficulty;
      form.duration_weeks = c.duration_weeks;
      form.max_students = c.max_students;
      form.status = c.status;
    }
  },
  { immediate: true }
);

const coverImage = ref<File | null>(null);
const coverPreview = ref<string | null>(null);
const isSubmitting = ref(false);

// Initialize cover preview from existing image
watch(
  course,
  (c) => {
    if (c?.cover_image_url) {
      coverPreview.value = c.cover_image_url;
    }
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
  { label: "Архив", value: "archived" },
];

// Handle cover image
const handleCoverChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    coverImage.value = input.files[0];
    coverPreview.value = URL.createObjectURL(input.files[0]);
  }
};

const removeCover = () => {
  coverImage.value = null;
  coverPreview.value = null;
};

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
    const formData = new FormData();
    Object.entries(form).forEach(([key, value]) => {
      if (value !== null && value !== undefined) {
        formData.append(key, String(value));
      }
    });

    if (coverImage.value) {
      formData.append("cover_image", coverImage.value);
    }

    await api.fetch(`/courses/${slug.value}/`, {
      method: "PATCH",
      body: formData,
    });

    toast.add({
      title: "Курс обновлён!",
      color: "success",
    });

    router.push(`/teacher/courses/${slug.value}`);
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: e.data?.detail || "Не удалось обновить курс",
      color: "error",
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Delete course
const showDeleteConfirm = ref(false);
const isDeleting = ref(false);

const deleteCourse = async () => {
  isDeleting.value = true;
  try {
    await api.delete(`/courses/${slug.value}/`);
    toast.add({
      title: "Курс удалён",
      color: "success",
    });
    router.push("/teacher/courses");
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: e.data?.detail || "Не удалось удалить курс",
      color: "error",
    });
  } finally {
    isDeleting.value = false;
    showDeleteConfirm.value = false;
  }
};

// SEO
useHead(() => ({
  title: course.value ? `Редактирование: ${course.value.title}` : "Загрузка...",
}));
</script>

<template>
  <div class="max-w-4xl">
    <!-- Loading -->
    <div v-if="coursePending" class="space-y-6">
      <USkeleton class="h-10 w-1/3" />
      <USkeleton class="h-64 rounded-xl" />
    </div>

    <template v-else-if="course">
      <!-- Header -->
      <div class="mb-8">
        <NuxtLink
          :to="`/teacher/courses/${slug}`"
          class="inline-flex items-center gap-2 text-sm text-muted hover:text-default transition-colors mb-4"
        >
          <UIcon name="i-lucide-arrow-left" class="size-4" />
          Назад к курсу
        </NuxtLink>
        <h1 class="text-2xl font-bold text-default">Редактирование курса</h1>
        <p class="text-muted mt-1">{{ course.title }}</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="onSubmit" class="space-y-8">
        <!-- Basic Info -->
        <div class="bg-elevated rounded-xl border border-default p-6">
          <h2 class="text-lg font-semibold text-default mb-6">
            Основная информация
          </h2>

          <div class="space-y-6">
            <UFormField label="Название курса" required>
              <UInput
                v-model="form.title"
                placeholder="Например: Основы веб-разработки"
                class="w-full"
              />
            </UFormField>

            <UFormField
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
        </div>

        <!-- Cover Image -->
        <div class="bg-elevated rounded-xl border border-default p-6">
          <h2 class="text-lg font-semibold text-default mb-6">Обложка курса</h2>

          <div
            v-if="!coverPreview"
            class="border-2 border-dashed border-default rounded-xl p-12 text-center hover:border-primary/50 transition-colors cursor-pointer"
            @click="($refs.coverInput as HTMLInputElement).click()"
          >
            <input
              ref="coverInput"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleCoverChange"
            />
            <UIcon
              name="i-lucide-image-plus"
              class="size-12 text-muted mx-auto mb-4"
            />
            <p class="text-muted">Нажмите для загрузки изображения</p>
          </div>

          <div v-else class="relative">
            <img
              :src="coverPreview"
              alt="Cover preview"
              class="w-full aspect-video object-cover rounded-xl"
            />
            <UButton
              icon="i-lucide-x"
              color="error"
              variant="solid"
              size="sm"
              class="absolute top-3 right-3"
              @click="removeCover"
            />
          </div>
        </div>

        <!-- Settings -->
        <div class="bg-elevated rounded-xl border border-default p-6">
          <h2 class="text-lg font-semibold text-default mb-6">Настройки</h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <UFormField label="Категория" required>
              <USelect
                v-model="form.category"
                :items="categoryOptions"
                placeholder="Выберите категорию"
                class="w-full"
              />
            </UFormField>

            <UFormField label="Уровень сложности" required>
              <USelect
                v-model="form.difficulty"
                :items="difficultyOptions"
                class="w-full"
              />
            </UFormField>

            <UFormField label="Длительность (недель)">
              <UInput
                v-model.number="form.duration_weeks"
                type="number"
                :min="1"
                :max="52"
                placeholder="Например: 8"
                class="w-full"
              />
            </UFormField>

            <UFormField label="Максимум студентов">
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
        </div>

        <!-- Status -->
        <div class="bg-elevated rounded-xl border border-default p-6">
          <h2 class="text-lg font-semibold text-default mb-6">
            Статус публикации
          </h2>

          <UFormField label="Статус">
            <URadioGroup
              v-model="form.status"
              :items="statusOptions"
              class="flex gap-4"
            />
          </UFormField>

          <UAlert
            v-if="form.status === 'archived'"
            color="warning"
            variant="soft"
            icon="i-lucide-alert-triangle"
            title="Архивация"
            description="Архивированный курс будет скрыт из каталога, но студенты сохранят доступ к материалам."
            class="mt-4"
          />
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-between pt-4">
          <UButton
            color="error"
            variant="ghost"
            icon="i-lucide-trash-2"
            @click="showDeleteConfirm = true"
          >
            Удалить курс
          </UButton>

          <div class="flex items-center gap-4">
            <UButton
              :to="`/teacher/courses/${slug}`"
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
              Сохранить
            </UButton>
          </div>
        </div>
      </form>
    </template>

    <!-- Delete Confirmation Modal -->
    <UModal v-model:open="showDeleteConfirm">
      <template #content>
        <div class="p-6 text-center">
          <UIcon
            name="i-lucide-alert-triangle"
            class="size-16 text-error mx-auto mb-4"
          />
          <h3 class="text-xl font-semibold text-default mb-2">Удалить курс?</h3>
          <p class="text-muted mb-6">
            Это действие нельзя отменить. Все уроки, задания и материалы будут
            удалены безвозвратно.
          </p>
          <div class="flex justify-center gap-4">
            <UButton
              color="neutral"
              variant="ghost"
              @click="showDeleteConfirm = false"
            >
              Отмена
            </UButton>
            <UButton color="error" :loading="isDeleting" @click="deleteCourse">
              Удалить
            </UButton>
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>
