<script setup lang="ts">
import type { CourseStudent } from "~/types";

interface Props {
  slug: string;
}

const props = defineProps<Props>();
const api = useApi();

const {
  data: students,
  pending,
  error,
  refresh,
} = await useAsyncData<CourseStudent[]>(`course-students-${props.slug}`, () =>
  api.get<CourseStudent[]>(`/courses/${props.slug}/students/`)
);

// Format date
const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

// Progress color
const getProgressColor = (
  progress: number
): "success" | "primary" | "warning" | "error" => {
  if (progress >= 80) return "success";
  if (progress >= 50) return "primary";
  if (progress >= 20) return "warning";
  return "error";
};
</script>

<template>
  <UCard :ui="{ body: 'p-0' }">
    <template #header>
      <div class="flex items-center justify-between">
        <h2 class="font-semibold text-default">Студенты курса</h2>
        <div class="flex items-center gap-2">
          <UBadge color="neutral" variant="subtle">
            {{ students?.length || 0 }} студентов
          </UBadge>
          <UButton
            color="neutral"
            variant="ghost"
            icon="i-lucide-refresh-cw"
            size="sm"
            :loading="pending"
            @click="refresh()"
          />
        </div>
      </div>
    </template>

    <!-- Loading -->
    <div v-if="pending" class="p-6 space-y-3">
      <USkeleton v-for="i in 5" :key="i" class="h-16 rounded-lg" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="p-6 text-center">
      <UIcon
        name="i-lucide-alert-circle"
        class="size-12 text-error mx-auto mb-3"
      />
      <p class="text-muted mb-4">Не удалось загрузить список студентов</p>
      <UButton color="primary" variant="soft" @click="refresh()">
        Попробовать снова
      </UButton>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="!students || students.length === 0"
      class="p-12 text-center"
    >
      <UIcon name="i-lucide-users" class="size-12 text-muted mx-auto mb-3" />
      <h3 class="font-medium text-default mb-1">Нет записанных студентов</h3>
      <p class="text-sm text-muted">
        Когда студенты запишутся на курс, они появятся здесь
      </p>
    </div>

    <!-- Students Table -->
    <div v-else class="divide-y divide-default">
      <div
        v-for="student in students"
        :key="student.id"
        class="flex items-center gap-4 px-6 py-4 hover:bg-muted/5 transition-colors"
      >
        <!-- Avatar -->
        <UAvatar
          :alt="`${student.first_name} ${student.last_name}`"
          size="md"
          :ui="{ fallback: 'font-medium text-sm' }"
        />

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <p class="font-medium text-default truncate">
            {{ student.first_name }} {{ student.last_name }}
          </p>
          <p class="text-sm text-muted truncate">
            {{ student.email }}
          </p>
        </div>

        <!-- Enrolled Date -->
        <div class="hidden md:block text-right shrink-0">
          <p class="text-xs text-muted">Дата записи</p>
          <p class="text-sm text-default">
            {{ formatDate(student.enrolled_at) }}
          </p>
        </div>

        <!-- Progress -->
        <div class="w-32 shrink-0">
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs text-muted">Прогресс</span>
            <span
              class="text-xs font-medium"
              :class="`text-${getProgressColor(student.progress)}`"
            >
              {{ student.progress }}%
            </span>
          </div>
          <UProgress
            :model-value="student.progress"
            :color="getProgressColor(student.progress)"
            size="xs"
          />
        </div>

        <!-- Actions -->
        <UDropdownMenu
          :items="[
            [
              {
                label: 'Посмотреть работы',
                icon: 'i-lucide-clipboard-list',
                disabled: true,
              },
              {
                label: 'Написать сообщение',
                icon: 'i-lucide-mail',
                disabled: true,
              },
            ],
          ]"
        >
          <UButton
            color="neutral"
            variant="ghost"
            icon="i-lucide-more-vertical"
            size="sm"
          />
        </UDropdownMenu>
      </div>
    </div>
  </UCard>
</template>
