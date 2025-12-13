<script setup lang="ts">
defineProps<{
  statusFilter: string;
}>();
</script>

<template>
  <div class="text-center py-20">
    <UIcon
      :name="
        statusFilter === 'pending' ? 'i-lucide-inbox' : 'i-lucide-clipboard-x'
      "
      class="size-16 text-muted mx-auto mb-4"
    />
    <h2 class="text-xl font-semibold text-default mb-2">
      {{
        statusFilter === "pending"
          ? "Нет работ на проверке"
          : "Работы не найдены"
      }}
    </h2>
    <p class="text-muted">
      {{
        statusFilter === "pending"
          ? "Отличная работа! Вы проверили все сданные задания."
          : "Попробуйте изменить параметры фильтрации."
      }}
    </p>
  </div>
</template>
