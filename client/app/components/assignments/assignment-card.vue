<script setup lang="ts">
import type { Assignment } from "~/types";

interface Props {
  assignment: Assignment;
  courseSlug: string;
  showActions?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showActions: true,
});

// Helpers
const isOverdue = computed(() => {
  if (!props.assignment.due_date) return false;
  return new Date(props.assignment.due_date) < new Date();
});

const formatDate = (date: string | null | undefined): string => {
  if (!date) return "Без срока";
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(date));
};

const getDaysUntilDue = computed(() => {
  if (!props.assignment.due_date) return null;
  const diff = new Date(props.assignment.due_date).getTime() - Date.now();
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
});
</script>

<template>
  <NuxtLink
    :to="`/learning/${courseSlug}/assignments/${assignment.id}`"
    class="block bg-elevated rounded-xl border border-default p-5 hover:border-primary/50 transition-all group"
  >
    <div class="flex items-start justify-between gap-4">
      <div class="flex-1 min-w-0">
        <!-- Title & Status Badges -->
        <div class="flex items-center gap-2 mb-2 flex-wrap">
          <h3
            class="font-semibold text-default group-hover:text-primary transition-colors"
          >
            {{ assignment.title }}
          </h3>
          <UBadge
            v-if="assignment.is_submitted"
            color="success"
            variant="subtle"
            size="sm"
          >
            Сдано
          </UBadge>
          <UBadge
            v-else-if="isOverdue"
            color="error"
            variant="subtle"
            size="sm"
          >
            Просрочено
          </UBadge>
          <UBadge
            v-else-if="
              getDaysUntilDue !== null &&
              getDaysUntilDue <= 3 &&
              getDaysUntilDue > 0
            "
            color="warning"
            variant="subtle"
            size="sm"
          >
            {{ getDaysUntilDue }} дн.
          </UBadge>
          <UBadge
            v-if="assignment.is_required"
            color="error"
            variant="soft"
            size="sm"
          >
            Обязательное
          </UBadge>
        </div>

        <!-- Description -->
        <p class="text-sm text-muted line-clamp-2 mb-4">
          {{ assignment.description }}
        </p>

        <!-- Meta Info -->
        <div class="flex items-center gap-4 text-sm text-muted">
          <!-- Due Date -->
          <div class="flex items-center gap-1.5">
            <UIcon name="i-lucide-calendar" class="size-4" />
            <span
              :class="isOverdue && !assignment.is_submitted ? 'text-error' : ''"
            >
              {{ formatDate(assignment.due_date) }}
            </span>
          </div>

          <!-- Max Score -->
          <div class="flex items-center gap-1.5">
            <UIcon name="i-lucide-star" class="size-4" />
            <span>{{ assignment.max_score }} баллов</span>
          </div>

          <!-- Files -->
          <div
            v-if="assignment.files.length > 0"
            class="flex items-center gap-1.5"
          >
            <UIcon name="i-lucide-paperclip" class="size-4" />
            <span>{{ assignment.files.length }}</span>
          </div>
        </div>
      </div>

      <!-- Arrow -->
      <UIcon
        name="i-lucide-chevron-right"
        class="size-5 text-muted group-hover:text-primary transition-colors shrink-0 mt-1"
      />
    </div>
  </NuxtLink>
</template>
