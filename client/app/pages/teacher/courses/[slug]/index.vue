<script setup lang="ts">
import type { CourseDetail, Lesson, Assignment } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
});

const route = useRoute();
const toast = useToast();
const lessonsApi = lessonsService();
const assignmentsApi = assignmentsService();

const slug = computed(() => route.params.slug as string);

// Fetch course details
const {
  data: course,
  pending: coursePending,
  refresh: refreshCourse,
} = await useAsyncData<CourseDetail>(`teacher-course-${slug.value}`, () =>
  useApi().get<CourseDetail>(`/courses/${slug.value}/`)
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
  () => lessonsApi.getLessonsByCourse(slug.value)
);

const lessons = computed(() => lessonsData.value?.results || []);

// Fetch assignments
interface AssignmentsResponse {
  count: number;
  results: Assignment[];
}

const {
  data: assignmentsData,
  pending: assignmentsPending,
  refresh: refreshAssignments,
} = await useAsyncData<AssignmentsResponse>(
  `teacher-course-assignments-${slug.value}`,
  () => assignmentsApi.getAssignments({ course: slug.value })
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

// ============================================================================
// Lessons CRUD
// ============================================================================

const showAddLesson = ref(false);
const showEditLesson = ref(false);
const showDeleteLesson = ref(false);
const selectedLesson = ref<Lesson | null>(null);
const lessonDeleteLoading = ref(false);

const addLessonModalRef = ref<{ setLoading: (v: boolean) => void }>();
const editLessonModalRef = ref<{ setLoading: (v: boolean) => void }>();

// Add Lesson
const handleAddLesson = async (lesson: {
  title: string;
  description: string;
  slug: string;
  duration_minutes: number;
}) => {
  addLessonModalRef.value?.setLoading(true);
  try {
    await lessonsApi.createLesson({
      course: slug.value,
      title: lesson.title,
      slug:
        lesson.slug ||
        lesson.title
          .toLowerCase()
          .replace(/[^a-z0-9а-яё]+/g, "-")
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

// Edit Lesson
const openEditLesson = (lesson: Lesson) => {
  selectedLesson.value = lesson;
  showEditLesson.value = true;
};

const handleEditLesson = async (data: {
  title: string;
  description: string;
  duration_minutes: number;
  is_published: boolean;
}) => {
  if (!selectedLesson.value) return;

  editLessonModalRef.value?.setLoading(true);
  try {
    await lessonsApi.updateLesson(selectedLesson.value.slug, data);
    toast.add({ title: "Урок обновлён", color: "success" });
    showEditLesson.value = false;
    selectedLesson.value = null;
    await refreshLessons();
  } catch (e: unknown) {
    const error = e as { data?: { detail?: string } };
    toast.add({
      title: "Ошибка",
      description: error.data?.detail || "Не удалось обновить урок",
      color: "error",
    });
  } finally {
    editLessonModalRef.value?.setLoading(false);
  }
};

// Delete Lesson
const openDeleteLesson = (lesson: Lesson) => {
  selectedLesson.value = lesson;
  showDeleteLesson.value = true;
};

const handleDeleteLesson = async () => {
  if (!selectedLesson.value) return;

  lessonDeleteLoading.value = true;
  try {
    await lessonsApi.deleteLesson(selectedLesson.value.slug);
    toast.add({ title: "Урок удалён", color: "success" });
    showDeleteLesson.value = false;
    selectedLesson.value = null;
    await refreshLessons();
  } catch (e: unknown) {
    const error = e as { data?: { detail?: string } };
    toast.add({
      title: "Ошибка",
      description: error.data?.detail || "Не удалось удалить урок",
      color: "error",
    });
  } finally {
    lessonDeleteLoading.value = false;
  }
};

// ============================================================================
// Assignments CRUD
// ============================================================================

const showEditAssignment = ref(false);
const showDeleteAssignment = ref(false);
const selectedAssignment = ref<Assignment | null>(null);
const assignmentDeleteLoading = ref(false);

const editAssignmentModalRef = ref<{ setLoading: (v: boolean) => void }>();

// Edit Assignment
const openEditAssignment = (assignment: Assignment) => {
  selectedAssignment.value = assignment;
  showEditAssignment.value = true;
};

const handleEditAssignment = async (data: {
  title: string;
  description: string;
  max_score: number;
  due_date: string;
  is_required: boolean;
  allow_late_submission: boolean;
}) => {
  if (!selectedAssignment.value) return;

  editAssignmentModalRef.value?.setLoading(true);
  try {
    await assignmentsApi.updateAssignment(selectedAssignment.value.id, {
      ...data,
      due_date: data.due_date || null,
    });
    toast.add({ title: "Задание обновлено", color: "success" });
    showEditAssignment.value = false;
    selectedAssignment.value = null;
    await refreshAssignments();
  } catch (e: unknown) {
    const error = e as { data?: { detail?: string } };
    toast.add({
      title: "Ошибка",
      description: error.data?.detail || "Не удалось обновить задание",
      color: "error",
    });
  } finally {
    editAssignmentModalRef.value?.setLoading(false);
  }
};

// Delete Assignment
const openDeleteAssignment = (assignment: Assignment) => {
  selectedAssignment.value = assignment;
  showDeleteAssignment.value = true;
};

const handleDeleteAssignment = async () => {
  if (!selectedAssignment.value) return;

  assignmentDeleteLoading.value = true;
  try {
    await assignmentsApi.deleteAssignment(selectedAssignment.value.id);
    toast.add({ title: "Задание удалено", color: "success" });
    showDeleteAssignment.value = false;
    selectedAssignment.value = null;
    await refreshAssignments();
  } catch (e: unknown) {
    const error = e as { data?: { detail?: string } };
    toast.add({
      title: "Ошибка",
      description: error.data?.detail || "Не удалось удалить задание",
      color: "error",
    });
  } finally {
    assignmentDeleteLoading.value = false;
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
        @edit="openEditLesson"
        @delete="openDeleteLesson"
      />

      <!-- Assignments Tab -->
      <TeacherCoursesDetailAssignmentsTab
        v-if="activeTab === 'assignments'"
        :assignments="assignments"
        :loading="assignmentsPending"
        :slug="slug"
        @edit="openEditAssignment"
        @delete="openDeleteAssignment"
      />

      <!-- Students Tab -->
      <TeacherCoursesDetailStudentsTab
        v-if="activeTab === 'students'"
        :slug="slug"
      />

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

    <!-- ================================================================== -->
    <!-- Modals -->
    <!-- ================================================================== -->

    <!-- Add Lesson Modal -->
    <TeacherCoursesDetailAddLessonModal
      ref="addLessonModalRef"
      v-model:open="showAddLesson"
      @submit="handleAddLesson"
    />

    <!-- Edit Lesson Modal -->
    <TeacherCoursesDetailEditLessonModal
      ref="editLessonModalRef"
      v-model:open="showEditLesson"
      :lesson="selectedLesson"
      @submit="handleEditLesson"
    />

    <!-- Delete Lesson Confirm -->
    <SharedConfirmDeleteModal
      v-model:open="showDeleteLesson"
      title="Удалить урок?"
      description="Все материалы и задания этого урока также будут удалены. Это действие нельзя отменить."
      :item-name="selectedLesson?.title"
      :loading="lessonDeleteLoading"
      @confirm="handleDeleteLesson"
    />

    <!-- Edit Assignment Modal -->
    <TeacherCoursesDetailEditAssignmentModal
      ref="editAssignmentModalRef"
      v-model:open="showEditAssignment"
      :assignment="selectedAssignment"
      @submit="handleEditAssignment"
    />

    <!-- Delete Assignment Confirm -->
    <SharedConfirmDeleteModal
      v-model:open="showDeleteAssignment"
      title="Удалить задание?"
      description="Все сдачи студентов по этому заданию также будут удалены. Это действие нельзя отменить."
      :item-name="selectedAssignment?.title"
      :loading="assignmentDeleteLoading"
      @confirm="handleDeleteAssignment"
    />
  </div>
</template>
