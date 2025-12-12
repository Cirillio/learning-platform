<script setup lang="ts">
import type { Teacher, User } from "~/types";

interface Props {
  teacher: Teacher;
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
      <div>
        <h3 class="text-xl font-semibold">
          {{ teacher.first_name }} {{ teacher.last_name }}
        </h3>
        <p class="text-primary-600 mb-2">Senior Lecturer</p>
      </div>
    </div>
  </div>
</template>
