<script setup lang="ts">
import type { CourseDetail, Lesson, Assignment } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
});

const route = useRoute();
const api = useApi();
const toast = useToast();

const slug = computed(() => route.params.slug as string);

// Fetch course details
const {
  data: course,
  pending: coursePending,
  refresh: refreshCourse,
} = await useAsyncData<CourseDetail>(`teacher-course-${slug.value}`, () =>
  api.get<CourseDetail>(`/courses/${slug.value}/`)
);

// Fetch lessons
interface LessonsResponse {
  count: number;
  results: Lesson[];
}

const {
  data: lessonsData,
  pending: lessonsPending,
  refresh: refreshLessons,
} = await useAsyncData<LessonsResponse>(
  `teacher-course-lessons-${slug.value}`,
  () => api.get<LessonsResponse>("/lessons/", { course: slug.value })
);

const lessons = computed(() => lessonsData.value?.results || []);

// Fetch assignments
interface AssignmentsResponse {
  count: number;
  results: Assignment[];
}

const { data: assignmentsData, pending: assignmentsPending } =
  await useAsyncData<AssignmentsResponse>(
    `teacher-course-assignments-${slug.value}`,
    () => api.get<AssignmentsResponse>("/assignments/", { course: slug.value })
  );

const assignments = computed(() => assignmentsData.value?.results || []);

// SEO
useHead(() => ({
  title: course.value ? `${course.value.title} | Управление` : "Загрузка...",
}));

// Active tab
const activeTab = ref("lessons");
const tabs = [
  { label: "Уроки", value: "lessons", icon: "i-lucide-book-open" },
  { label: "Задания", value: "assignments", icon: "i-lucide-clipboard-list" },
  { label: "Студенты", value: "students", icon: "i-lucide-users" },
  { label: "Статистика", value: "stats", icon: "i-lucide-bar-chart-2" },
];

// Add Lesson Modal
const showAddLesson = ref(false);
const addLessonModalRef =
  ref<
    InstanceType<
      typeof import("~/components/teacher/courses/detail/add-lesson-modal.vue").default
    >
  >();

const handleAddLesson = async (lesson: {
  title: string;
  description: string;
  duration_minutes: number;
}) => {
  addLessonModalRef.value?.setLoading(true);
  try {
    await api.post("/lessons/", {
      course: slug.value,
      title: lesson.title,
      slug: lesson.title
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/(^-|-$)+/g, ""),
      description: lesson.description,
      duration_minutes: lesson.duration_minutes,
      order: lessons.value.length + 1,
    });

    toast.add({ title: "Урок добавлен", color: "success" });
    showAddLesson.value = false;
    await refreshLessons();
  } catch (e: unknown) {
    const error = e as { data?: { detail?: string } };
    toast.add({
      title: "Ошибка",
      description: error.data?.detail || "Не удалось добавить урок",
      color: "error",
    });
  } finally {
    addLessonModalRef.value?.setLoading(false);
  }
};

// Delete lesson
const handleDeleteLesson = async (lessonId: number) => {
  try {
    await api.delete(`/lessons/${lessonId}/`);
    toast.add({ title: "Урок удалён", color: "success" });
    await refreshLessons();
  } catch (e: unknown) {
    const error = e as { data?: { detail?: string } };
    toast.add({
      title: "Ошибка",
      description: error.data?.detail || "Не удалось удалить урок",
      color: "error",
    });
  }
};
</script>

<template>
  <div>
    <!-- Loading -->
    <div v-if="coursePending" class="space-y-6">
      <USkeleton class="h-32 rounded-xl" />
      <USkeleton class="h-64 rounded-xl" />
    </div>

    <!-- Error -->
    <div v-else-if="!course" class="text-center py-20">
      <UIcon
        name="i-lucide-alert-circle"
        class="size-16 text-error mx-auto mb-4"
      />
      <h2 class="text-xl font-semibold text-default mb-2">Курс не найден</h2>
      <UButton to="/teacher/courses" color="primary">К списку курсов</UButton>
    </div>

    <!-- Content -->
    <template v-else>
      <!-- Header -->
      <TeacherCoursesDetailHeader :course="course" :slug="slug" class="mb-2" />

      <!-- Stats -->
      <TeacherCoursesDetailStats :course="course" class="mb-2" />

      <!-- Tabs -->
      <div class="mb-2">
        <UTabs
          v-model="activeTab"
          :items="
            tabs.map((t) => ({ label: t.label, value: t.value, icon: t.icon }))
          "
          size="lg"
          :ui="{
            content: 'hidden',
          }"
        />
      </div>

      <!-- Lessons Tab -->
      <TeacherCoursesDetailLessonsTab
        v-if="activeTab === 'lessons'"
        :lessons="lessons"
        :loading="lessonsPending"
        :slug="slug"
        @add="showAddLesson = true"
        @delete="handleDeleteLesson"
      />

      <!-- Assignments Tab -->
      <TeacherCoursesDetailAssignmentsTab
        v-if="activeTab === 'assignments'"
        :assignments="assignments"
        :loading="assignmentsPending"
        :slug="slug"
      />

      <!-- Students Tab -->
      <div
        v-if="activeTab === 'students'"
        class="bg-elevated rounded-xl border border-default p-12 text-center"
      >
        <UIcon name="i-lucide-users" class="size-12 text-muted mx-auto mb-3" />
        <p class="text-muted">Список студентов появится здесь</p>
      </div>

      <!-- Stats Tab -->
      <div
        v-if="activeTab === 'stats'"
        class="bg-elevated rounded-xl border border-default p-12 text-center"
      >
        <UIcon
          name="i-lucide-bar-chart-2"
          class="size-12 text-muted mx-auto mb-3"
        />
        <p class="text-muted">Статистика курса появится здесь</p>
      </div>
    </template>

    <!-- Add Lesson Modal -->
    <TeacherCoursesDetailAddLessonModal
      ref="addLessonModalRef"
      v-model:open="showAddLesson"
      @submit="handleAddLesson"
    />
  </div>
</template>
