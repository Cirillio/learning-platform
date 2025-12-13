<script setup lang="ts">
interface Props {
  userName: string;
  title?: string;
  subtitle?: string;
}

withDefaults(defineProps<Props>(), {
  title: "Добро пожаловать",
  subtitle:
    "Управляйте своими курсами, заданиями и отслеживайте прогресс студентов",
});
</script>

<template>
  <div
    class="relative rounded-lg bg-linear-to-br from-primary/20 to-primary/5 p-6 lg:p-8 shadow-xs overflow-hidden"
  >
    <div class="absolute inset-0 bg-grid-pattern opacity-5" />
    <div class="relative z-10">
      <h1 class="text-2xl lg:text-3xl font-bold text-default mb-2">
        {{ title }}, {{ userName }}!
      </h1>
      <p class="text-muted">{{ subtitle }}</p>
    </div>
  </div>
</template>

<style scoped>
.bg-grid-pattern {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Cg fill='%239C92AC' fill-opacity='0.2'%3E%3Cpath d='M0 0h40v40H0V0zm1 1v38h38V1H1z'/%3E%3C/g%3E%3C/svg%3E");
}
</style>
