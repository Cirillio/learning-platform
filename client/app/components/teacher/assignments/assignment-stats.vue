<script setup lang="ts">
defineProps<{
  totalCount: number;
  pendingCount: number;
  gradedCount: number;
  lateCount: number;
}>();
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <UCard>
      <div class="flex items-center gap-3">
        <div class="p-2 bg-primary/10 rounded-lg">
          <UIcon name="i-lucide-file-text" class="size-5 text-primary" />
        </div>
        <div>
          <div class="text-2xl font-bold">{{ totalCount }}</div>
          <div class="text-sm text-muted">Всего сдач</div>
        </div>
      </div>
    </UCard>
    <UCard>
      <div class="flex items-center gap-3">
        <div class="p-2 bg-warning/10 rounded-lg">
          <UIcon name="i-lucide-clock" class="size-5 text-warning" />
        </div>
        <div>
          <div class="text-2xl font-bold">{{ pendingCount }}</div>
          <div class="text-sm text-muted">Ожидают проверки</div>
        </div>
      </div>
    </UCard>
    <UCard>
      <div class="flex items-center gap-3">
        <div class="p-2 bg-success/10 rounded-lg">
          <UIcon name="i-lucide-check-circle" class="size-5 text-success" />
        </div>
        <div>
          <div class="text-2xl font-bold">{{ gradedCount }}</div>
          <div class="text-sm text-muted">Проверено</div>
        </div>
      </div>
    </UCard>
    <UCard>
      <div class="flex items-center gap-3">
        <div class="p-2 bg-error/10 rounded-lg">
          <UIcon name="i-lucide-alert-triangle" class="size-5 text-error" />
        </div>
        <div>
          <div class="text-2xl font-bold">{{ lateCount }}</div>
          <div class="text-sm text-muted">Просрочено</div>
        </div>
      </div>
    </UCard>
  </div>
</template>
