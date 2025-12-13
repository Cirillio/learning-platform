<script setup lang="ts">
import type { Submission } from "~/types";

defineProps<{
  submissions: Submission[];
}>();

const formatDate = (date: string) => {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date));
};
</script>

<template>
  <UCard>
    <table class="w-full">
      <thead>
        <tr class="border-b border-default text-left text-lg font-medium">
          <th class="px-6 py-4">Студент</th>
          <th class="px-6 py-4">Задание</th>
          <th class="px-6 py-4">Статус</th>
          <th class="px-6 py-4">Дата</th>
          <th class="px-6 py-4">Действия</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-default">
        <TeacherGradingTableItem
          v-for="submission in submissions"
          :key="submission.id"
          :submission="submission"
        />
      </tbody>
    </table>
  </UCard>
</template>
