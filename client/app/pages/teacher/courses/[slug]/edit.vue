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
  cover_image: z.string().optional(),
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
  cover_image: "",
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
      form.cover_image = c.cover_image_url || c.cover_image || "";
    }
  },
  { immediate: true }
);

const coverPreview = ref<string | null>(null);
const isSubmitting = ref(false);

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
  { label: "Архив", value: "archived" },
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
    await api.patch(`/courses/${slug.value}/`, form);

    toast.add({
      title: "Курс обновлён!",
      color: "success",
    });

    router.push(`/teacher/courses/${slug.value}`);
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
        description: e.data?.detail || "Не удалось обновить курс",
        color: "error",
      });
    }
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
  <div class="">
    <!-- Loading -->
    <div v-if="coursePending" class="space-y-6">
      <USkeleton class="h-10 w-1/3" />
      <USkeleton class="h-64 rounded-xl" />
    </div>

    <template v-else-if="course">
      <!-- Header -->
      <div class="mb-2">
        <NuxtLink
          :to="`/teacher/courses/${slug}`"
          class="inline-flex items-center gap-2 text-sm text-muted hover:text-default transition-colors"
        >
          <UIcon name="i-lucide-arrow-left" class="size-4" />
          Назад к курсу
        </NuxtLink>
        <h1 class="text-4xl font-bold text-default">Редактирование курса</h1>
        <p class="text-muted text-lg mt-1">{{ course.title }}</p>
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
                <h2 class="text-2xl font-semibold text-default">
                  Обложка курса
                </h2>
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

              <UAlert
                v-if="form.status === 'archived'"
                color="warning"
                variant="soft"
                icon="i-lucide-alert-triangle"
                title="Архивация"
                description="Архивированный курс будет скрыт из каталога, но студенты сохранят доступ к материалам."
                class="mt-4"
              />
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
              icon="i-lucide-save"
              size="xl"
            >
              Сохранить
            </UButton>
            <UButton
              :to="`/teacher/courses/${slug}`"
              color="neutral"
              variant="ghost"
              size="xl"
            >
              Отмена
            </UButton>
          </div>
          <UButton
            color="error"
            variant="ghost"
            icon="i-lucide-trash-2"
            @click="showDeleteConfirm = true"
          >
            Удалить курс
          </UButton>
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
