<script setup lang="ts">
import type { User } from "~/types";

defineProps<{
  profile: User;
}>();
</script>

<template>
  <UCard
    :ui="{
      header: 'bg-primary text-white border-0',
    }"
  >
    <template #header>
      <h3 class="font-bold text-2xl">Учебные данные</h3>
    </template>
    <dl class="space-y-4">
      <div v-if="profile.student_id">
        <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">
          Студенческий билет
        </dt>
        <dd
          class="mt-1 text-sm font-mono bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded inline-block"
        >
          {{ profile.student_id }}
        </dd>
      </div>
      <div v-if="profile.enrollment_year">
        <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">
          Год поступления
        </dt>
        <dd class="mt-1 text-sm text-gray-900 dark:text-white">
          {{ profile.enrollment_year }}
        </dd>
      </div>
      <div v-if="profile.experience_years !== null">
        <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">
          Опыт работы (лет)
        </dt>
        <dd class="mt-1 text-sm text-gray-900 dark:text-white">
          {{ profile.experience_years }}
        </dd>
      </div>
    </dl>
  </UCard>
</template>
