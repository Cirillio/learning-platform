<script setup lang="ts">
import type { User } from "~/types";

interface Props {
  teacher: User;
}

defineProps<Props>();
</script>

<template>
  <div
    class="space-y-4 pt-8 border-t border-neutral-200 dark:border-neutral-800"
  >
    <h2 class="text-2xl font-bold text-neutral-900 dark:text-white">
      Преподаватель
    </h2>
    <div class="flex items-start gap-6">
      <UAvatar
        :src="teacher.avatar || undefined"
        :alt="teacher.first_name"
        size="3xl"
      />
      <div>
        <h3 class="text-xl font-semibold">
          {{ teacher.first_name }} {{ teacher.last_name }}
        </h3>
        <p class="text-primary-600 mb-2">Senior Lecturer</p>
        <p
          class="text-neutral-600 dark:text-neutral-400 text-sm leading-relaxed"
        >
          {{ teacher.bio || "Биография преподавателя отсутствует." }}
        </p>
      </div>
    </div>
  </div>
</template>
