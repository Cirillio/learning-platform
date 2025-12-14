<script setup lang="ts">
import type { Course, Grade, Submission, CourseDetail } from "~/types";

// Extended course type for my_courses endpoint that may include progress
interface EnrolledCourse extends Course {
  progress?: number;
}

definePageMeta({
  middleware: ["auth"],
});

const authStore = useAuthStore();
const api = useApi();

// Redirect teachers to their dashboard
if (authStore.isTeacher) {
  navigateTo("/teacher/dashboard", { replace: true });
}

// Fetch enrolled courses
interface CoursesResponse {
  count: number;
  results: EnrolledCourse[];
}

const { data: coursesData, pending: coursesPending } =
  await useAsyncData<CoursesResponse>("student-my-courses", () =>
    api.get<CoursesResponse>("/courses/my_courses/")
  );

const courses = computed(() => coursesData.value?.results || []);

// Fetch recent grades
interface GradesResponse {
  count: number;
  results: Grade[];
}

const { data: gradesData, pending: gradesPending } =
  await useAsyncData<GradesResponse>("student-recent-grades", () =>
    api.get<GradesResponse>("/grades/", { page_size: 5 })
  );

const recentGrades = computed(() => gradesData.value?.results || []);

// Fetch pending submissions
interface SubmissionsResponse {
  count: number;
  results: Submission[];
}

const { data: submissionsData, pending: submissionsPending } =
  await useAsyncData<SubmissionsResponse>("student-pending-submissions", () =>
    api.get<SubmissionsResponse>("/submissions/", {
      status: "pending",
      page_size: 5,
    })
  );

const pendingSubmissions = computed(() => submissionsData.value?.results || []);

// Statistics
const stats = computed(() => [
  {
    label: "Курсы",
    value: courses.value.length,
    icon: "i-lucide-book-open",
    iconColor: "text-primary",
    bgColor: "bg-primary/10",
    link: courses.value.length > 0 ? "/courses" : undefined,
  },
  {
    label: "Ожидают проверки",
    value: submissionsData.value?.count || 0,
    icon: "i-lucide-clock",
    iconColor: "text-warning",
    bgColor: "bg-warning/10",
  },
  {
    label: "Получено оценок",
    value: gradesData.value?.count || 0,
    icon: "i-lucide-trophy",
    iconColor: "text-success",
    bgColor: "bg-success/10",
    link: gradesData.value?.count ? "/learning/grades" : undefined,
  },
]);

// Score color
const getScoreBadgeColor = (
  score: number
): "success" | "primary" | "warning" | "error" => {
  if (score >= 90) return "success";
  if (score >= 70) return "primary";
  if (score >= 50) return "warning";
  return "error";
};

// Format date
const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "short",
  });
};

// SEO
useHead({
  title: "Моё обучение | Панель студента",
});
</script>

<template>
  <LayoutContainer class="py-8 bg-default">
    <!-- Welcome Section -->
    <div class="mb-2">
      <h1 class="text-2xl lg:text-3xl font-bold text-default">
        Привет, {{ authStore.user?.first_name || authStore.user?.username }}! 👋
      </h1>
      <p class="text-muted mt-1">Добро пожаловать в твой учебный кабинет</p>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 mb-2">
      <UCard v-for="stat in stats" :key="stat.label" :ui="{ body: 'p-4' }">
        <div class="flex items-center gap-2">
          <div
            class="size-12 rounded-xl flex items-center justify-center"
            :class="stat.bgColor"
          >
            <UIcon :name="stat.icon" class="size-6" :class="stat.iconColor" />
          </div>
          <div class="flex-1">
            <p class="text-2xl font-bold text-default">{{ stat.value }}</p>
            <p class="text-sm text-muted">{{ stat.label }}</p>
          </div>
          <UButton
            v-if="stat.link"
            :to="stat.link"
            color="neutral"
            variant="ghost"
            icon="i-lucide-arrow-right"
            size="sm"
          />
        </div>
      </UCard>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-2">
      <!-- My Courses -->
      <div class="lg:col-span-2">
        <UCard>
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="font-semibold text-2xl text-default">Мои курсы</h2>
              <UButton
                to="/courses"
                color="primary"
                variant="ghost"
                size="lg"
                trailing-icon="i-lucide-arrow-right"
              >
                Все курсы
              </UButton>
            </div>
          </template>

          <!-- Loading -->
          <div v-if="coursesPending" class="space-y-2">
            <USkeleton v-for="i in 3" :key="i" class="h-20 rounded-lg" />
          </div>

          <!-- Empty State -->
          <div v-else-if="courses.length === 0" class="text-center py-8">
            <UIcon
              name="i-lucide-book-open"
              class="size-12 text-muted mx-auto mb-3"
            />
            <p class="text-muted mb-4">Вы ещё не записаны на курсы</p>
            <UButton to="/courses" color="primary"> Найти курсы </UButton>
          </div>

          <!-- Courses List -->
          <div v-else class="space-y-2">
            <NuxtLink
              v-for="course in courses.slice(0, 5)"
              :key="course.id"
              :to="`/learning/${course.slug}`"
              class="flex items-center gap-4 p-3 rounded-lg hover:bg-muted/5 transition-colors group"
            >
              <!-- Course Image -->
              <div
                class="size-14 rounded-lg bg-muted/10 flex items-center justify-center shrink-0 overflow-hidden"
              >
                <img
                  v-if="course.cover_image_url"
                  :src="course.cover_image_url"
                  :alt="course.title"
                  class="size-full object-cover"
                />
                <UIcon
                  v-else
                  name="i-lucide-book-open"
                  class="size-6 text-muted"
                />
              </div>

              <!-- Course Info -->
              <div class="flex-1 min-w-0">
                <h3
                  class="font-medium text-default group-hover:text-primary transition-colors truncate"
                >
                  {{ course.title }}
                </h3>
                <p class="text-sm text-muted truncate">
                  {{ course.teacher_name }}
                </p>
              </div>

              <!-- Progress -->
              <div class="text-right shrink-0">
                <p class="text-sm font-medium text-primary">
                  {{ course.progress || 0 }}%
                </p>
                <UProgress
                  :model-value="course.progress || 0"
                  size="xs"
                  color="primary"
                  class="w-16"
                />
              </div>
            </NuxtLink>
          </div>
        </UCard>
      </div>

      <!-- Sidebar -->
      <div class="space-y-2">
        <!-- Recent Grades -->
        <UCard>
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="font-semibold text-2xl text-default">
                Последние оценки
              </h2>
              <UButton
                v-if="recentGrades.length > 0"
                to="/learning/grades"
                color="primary"
                variant="ghost"
                size="lg"
              >
                Все
              </UButton>
            </div>
          </template>

          <!-- Loading -->
          <div v-if="gradesPending" class="space-y-2">
            <USkeleton v-for="i in 3" :key="i" class="h-12 rounded-lg" />
          </div>

          <!-- Empty -->
          <div v-else-if="recentGrades.length === 0" class="text-center py-6">
            <UIcon
              name="i-lucide-trophy"
              class="size-10 text-muted mx-auto mb-2"
            />
            <p class="text-sm text-muted">Оценок пока нет</p>
          </div>

          <!-- Grades List -->
          <div v-else class="space-y-2">
            <div
              v-for="grade in recentGrades"
              :key="grade.id"
              class="flex items-center gap-3 p-2 rounded-lg"
            >
              <UBadge
                :color="getScoreBadgeColor(grade.score)"
                variant="subtle"
                size="sm"
              >
                {{ grade.score }}
              </UBadge>
              <div class="flex-1 min-w-0">
                <p class="text-sm text-default truncate">
                  {{ grade.assignment_title }}
                </p>
                <p class="text-xs text-muted">
                  {{ formatDate(grade.graded_at) }}
                </p>
              </div>
            </div>
          </div>
        </UCard>

        <!-- Pending Submissions -->
        <UCard>
          <template #header>
            <h2 class="font-semibold text-default">На проверке</h2>
          </template>

          <!-- Loading -->
          <div v-if="submissionsPending" class="space-y-2">
            <USkeleton v-for="i in 3" :key="i" class="h-12 rounded-lg" />
          </div>

          <!-- Empty -->
          <div
            v-else-if="pendingSubmissions.length === 0"
            class="text-center py-6"
          >
            <UIcon
              name="i-lucide-check-circle"
              class="size-10 text-success mx-auto mb-2"
            />
            <p class="text-sm text-muted">Все работы проверены!</p>
          </div>

          <!-- List -->
          <div v-else class="space-y-2">
            <div
              v-for="submission in pendingSubmissions"
              :key="submission.id"
              class="flex items-center gap-3 p-2 rounded-lg"
            >
              <div
                class="size-8 rounded-full bg-warning/10 flex items-center justify-center shrink-0"
              >
                <UIcon name="i-lucide-clock" class="size-4 text-warning" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm text-default truncate">
                  {{ submission.assignment_title }}
                </p>
                <p class="text-xs text-muted">
                  Отправлено {{ formatDate(submission.submitted_at) }}
                </p>
              </div>
            </div>
          </div>
        </UCard>
      </div>
    </div>
  </LayoutContainer>
</template>
