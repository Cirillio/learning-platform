<script setup lang="ts">
import type { Lesson } from "~/types";

interface Props {
  lessons: Lesson[];
  currentLessonSlug: string;
  courseSlug: string;
}

const props = defineProps<Props>();

// Сортировка уроков по порядку
const sortedLessons = computed(() =>
  [...props.lessons].sort((a, b) => a.order - b.order)
);

// Проверка: урок уже пройден (порядок меньше текущего)
const isLessonCompleted = (lesson: Lesson): boolean => {
  const currentLesson = props.lessons.find(
    (l) => l.slug === props.currentLessonSlug
  );
  if (!currentLesson) return false;
  return lesson.order < currentLesson.order;
};

// Проверка: это текущий урок
const isCurrentLesson = (lesson: Lesson): boolean => {
  return lesson.slug === props.currentLessonSlug;
};

// Максимальное количество видимых уроков
const maxVisible = ref(5);
const showAll = ref(false);

const visibleLessons = computed(() => {
  if (showAll.value) return sortedLessons.value;

  // Показываем уроки вокруг текущего
  const currentIndex = sortedLessons.value.findIndex(
    (l) => l.slug === props.currentLessonSlug
  );

  const start = Math.max(0, currentIndex - 2);
  const end = Math.min(sortedLessons.value.length, start + maxVisible.value);

  return sortedLessons.value.slice(start, end);
});

const hasMoreLessons = computed(
  () => sortedLessons.value.length > maxVisible.value
);
</script>

<template>
  <UCard class="dark:bg-muted/25 bg-muted/75">
    <!-- Header -->
    <div class="p-4 border-b border-default flex items-center justify-between">
      <h3 class="font-semibold text-default">Содержание курса</h3>
      <UBadge variant="soft" color="neutral" size="sm">
        {{ lessons.length }} уроков
      </UBadge>
    </div>

    <!-- Lessons List -->
    <nav class="divide-y divide-default max-h-[400px] overflow-y-auto">
      <NuxtLink
        v-for="lesson in visibleLessons"
        :key="lesson.id"
        :to="`/courses/${courseSlug}/lessons/${lesson.slug}`"
        class="flex items-center gap-3 p-3 hover:bg-muted/50 transition-colors group"
        :class="{
          'bg-primary/5 border-l-2 border-l-primary': isCurrentLesson(lesson),
        }"
      >
        <!-- Status Icon -->
        <div
          class="size-8 rounded-full flex items-center justify-center shrink-0 transition-colors"
          :class="[
            isCurrentLesson(lesson)
              ? 'bg-primary text-white'
              : isLessonCompleted(lesson)
              ? 'bg-success/10 text-success'
              : 'bg-muted text-muted group-hover:bg-primary/10 group-hover:text-primary',
          ]"
        >
          <UIcon
            v-if="isCurrentLesson(lesson)"
            name="i-lucide-play"
            class="size-4"
          />
          <UIcon
            v-else-if="isLessonCompleted(lesson)"
            name="i-lucide-check"
            class="size-4"
          />
          <span v-else class="text-xs font-medium">
            {{ lesson.order }}
          </span>
        </div>

        <!-- Lesson Info -->
        <div class="flex-1 min-w-0">
          <p
            class="text-sm font-medium truncate transition-colors"
            :class="[
              isCurrentLesson(lesson)
                ? 'text-primary'
                : 'text-default group-hover:text-primary',
            ]"
          >
            {{ lesson.title }}
          </p>
          <p class="text-xs text-muted">
            {{ lesson.duration_minutes || "—" }} мин
          </p>
        </div>

        <!-- Arrow for current -->
        <UIcon
          v-if="isCurrentLesson(lesson)"
          name="i-lucide-chevron-right"
          class="size-4 text-primary shrink-0"
        />
      </NuxtLink>
    </nav>

    <!-- Show More -->
    <div v-if="hasMoreLessons" class="p-3 border-t border-default">
      <UButton
        variant="ghost"
        color="neutral"
        size="sm"
        block
        @click="showAll = !showAll"
      >
        {{ showAll ? "Свернуть" : `Показать все (${lessons.length})` }}
        <UIcon
          :name="showAll ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'"
          class="size-4 ml-1"
        />
      </UButton>
    </div>
  </UCard>
</template>
