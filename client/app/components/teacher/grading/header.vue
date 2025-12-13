<script setup lang="ts">
defineProps<{
  totalCount: number;
  statusFilter: string;
}>();
</script>

<template>
  <div class="flex items-center justify-between mb-8">
    <div>
      <p class="text-muted mt-1 text-xl font-bold">
        {{ totalCount }} работ{{
          statusFilter === "pending" ? " ожидают проверки" : ""
        }}
      </p>
    </div>
  </div>
</template>
