<script lang="ts" setup>
import type { AvatarProps } from "@nuxt/ui";
import type { User, UserProfile } from "~/types";

const props = defineProps<{
  user: User | null;
}>();

// Динамическая ссылка на профиль в зависимости от роли
const profileLink = computed(() => {
  return props.user?.role === "teacher" ? "/teacher/profile" : "/profile";
});

// Динамическая ссылка на "Мои уроки" / "Мои курсы"
const learningLink = computed(() => {
  return props.user?.role === "teacher" ? "/teacher" : "/learning";
});

const learningLabel = computed(() => {
  return props.user?.role === "teacher" ? "Панель учителя" : "Мои уроки";
});
</script>

<template>
  <UButton :label="learningLabel" :to="learningLink" />
  <USeparator orientation="vertical" color="neutral" class="h-6" />
  <UButton
    :to="profileLink"
    :label="user?.first_name"
    variant="ghost"
    color="neutral"
  />
</template>
