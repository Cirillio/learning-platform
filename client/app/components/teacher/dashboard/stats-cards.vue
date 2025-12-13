<script setup lang="ts">
import type { StatItem } from "./stat-card.vue";

interface Props {
  stats: StatItem[];
}

defineProps<Props>();
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2">
    <TeacherDashboardStatCard
      v-for="stat in stats"
      :key="stat.label"
      :stat="stat"
    />
  </div>
</template>
