<script setup lang="ts">
import type { CourseDetail, Lesson } from "~/types";
import { useCoursesService } from "~/services";

interface Props {
  isCollapsed: boolean;
}

interface LessonsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Lesson[];
}

defineProps<Props>();
const emit = defineEmits<{
  toggleSidebar: [];
}>();

const route = useRoute();
const coursesService = useCoursesService();
const courseSlug = computed(() => route.params.course_slug as string);

// Fetch course data for sidebar
const { data: course, pending } = await useAsyncData<CourseDetail>(
  `learning-sidebar-course-${courseSlug.value}`,
  () => coursesService.getCourse(courseSlug.value),
  { watch: [courseSlug] }
);

// Fetch lessons for navigation
const { data: lessonsResponse } = await useAsyncData<LessonsResponse>(
  `learning-sidebar-lessons-${courseSlug.value}`,
  () => coursesService.getCourseLessons(courseSlug.value),
  { watch: [courseSlug] }
);

const lessons = computed(() => lessonsResponse.value?.results || []);
</script>

<template>
  <aside
    class="fixed left-0 top-0 h-screen bg-elevated border-r border-default transition-all duration-300 z-40"
    :class="isCollapsed ? 'w-16' : 'w-72'"
  >
    <!-- Header -->
    <div
      class="h-16 flex items-center justify-between px-4 border-b border-default"
    >
      <NuxtLink
        v-if="!isCollapsed"
        to="/dashboard"
        class="flex items-center gap-2 text-default hover:text-primary transition-colors"
      >
        <UIcon name="i-lucide-graduation-cap" class="size-6" />
        <span class="font-semibold text-sm">Learning Platform</span>
      </NuxtLink>
      <UIcon
        v-else
        name="i-lucide-graduation-cap"
        class="size-6 text-primary mx-auto"
      />
    </div>

    <!-- Course Info -->
    <div v-if="course && !pending" class="p-4 border-b border-default">
      <template v-if="!isCollapsed">
        <NuxtLink :to="`/learning/${courseSlug}`" class="block group">
          <p class="text-xs text-muted uppercase tracking-wider mb-1">
            Текущий курс
          </p>
          <h3
            class="font-semibold text-default group-hover:text-primary transition-colors line-clamp-2"
          >
            {{ course.title }}
          </h3>
        </NuxtLink>

        <!-- Progress Bar -->
        <div v-if="course.progress !== undefined" class="mt-3">
          <div class="flex justify-between text-xs text-muted mb-1">
            <span>Прогресс</span>
            <span>{{ course.progress }}%</span>
          </div>
          <UProgress :model-value="course.progress" size="sm" color="primary" />
        </div>
      </template>
      <template v-else>
        <UTooltip text="Прогресс курса" :delay="100">
          <div class="flex flex-col items-center">
            <UIcon name="i-lucide-book-open" class="size-5 text-muted" />
            <span class="text-xs text-muted mt-1"
              >{{ course.progress || 0 }}%</span
            >
          </div>
        </UTooltip>
      </template>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto py-4">
      <!-- Quick Links -->
      <div class="px-4 mb-4">
        <template v-if="!isCollapsed">
          <p class="text-xs text-muted uppercase tracking-wider mb-2">
            Навигация
          </p>
        </template>
        <div class="space-y-1">
          <NuxtLink
            :to="`/learning/${courseSlug}`"
            class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors"
            :class="[
              route.path === `/learning/${courseSlug}`
                ? 'bg-primary/10 text-primary'
                : 'text-muted hover:bg-muted/10 hover:text-default',
            ]"
          >
            <UIcon name="i-lucide-layout-dashboard" class="size-5 shrink-0" />
            <span v-if="!isCollapsed" class="text-sm">Обзор курса</span>
          </NuxtLink>

          <NuxtLink
            :to="`/learning/${courseSlug}/assignments`"
            class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors"
            :class="[
              route.path.includes('/assignments')
                ? 'bg-primary/10 text-primary'
                : 'text-muted hover:bg-muted/10 hover:text-default',
            ]"
          >
            <UIcon name="i-lucide-clipboard-list" class="size-5 shrink-0" />
            <span v-if="!isCollapsed" class="text-sm">Задания</span>
          </NuxtLink>
        </div>
      </div>

      <!-- Lessons List -->
      <div class="px-4">
        <template v-if="!isCollapsed">
          <p class="text-xs text-muted uppercase tracking-wider mb-2">Уроки</p>
        </template>
        <div class="space-y-1">
          <NuxtLink
            v-for="lesson in lessons"
            :key="lesson.id"
            :to="`/learning/${courseSlug}/lessons/${lesson.slug}`"
            class="flex items-center gap-3 py-2 rounded-lg transition-colors group"
            :class="[
              route.params.lesson_slug === lesson.slug
                ? 'bg-primary/10 text-primary'
                : 'text-muted hover:bg-muted/10 hover:text-default',
            ]"
          >
            <div
              class="size-6 rounded-full flex items-center justify-center text-xs font-medium shrink-0"
              :class="[
                route.params.lesson_slug === lesson.slug
                  ? 'bg-primary text-white'
                  : 'bg-muted/20 text-muted group-hover:bg-muted/30',
              ]"
            >
              {{ lesson.order }}
            </div>
            <span v-if="!isCollapsed" class="text-sm truncate">{{
              lesson.title
            }}</span>
          </NuxtLink>
        </div>
      </div>
    </nav>

    <!-- Collapse Toggle -->
    <div class="p-4 border-t border-default">
      <UButton
        :icon="isCollapsed ? 'i-lucide-chevron-right' : 'i-lucide-chevron-left'"
        color="neutral"
        variant="ghost"
        size="sm"
        :class="isCollapsed ? 'w-full justify-center' : ''"
        @click="emit('toggleSidebar')"
      />
    </div>
  </aside>
</template>
