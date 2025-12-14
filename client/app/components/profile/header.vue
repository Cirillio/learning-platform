<script setup lang="ts">
import type { User } from "~/types";

const props = defineProps<{
  profile: User;
}>();

const emit = defineEmits<{
  (e: "logout"): void;
}>();

const fullName = computed(() => {
  return (
    `${props.profile.first_name} ${props.profile.last_name}`.trim() ||
    props.profile.username
  );
});

const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return "Не указано";
  return new Date(dateStr).toLocaleDateString("ru-RU");
};

// --- Edit Modal ---
const isModalOpen = ref(false);
</script>

<template>
  <UCard class="w-full bg-muted/25">
    <div class="flex flex-col gap-6 relative">
      <UButton
        color="error"
        variant="subtle"
        class="justify-center absolute top-0 right-0 mt-2 mr-2"
        size="sm"
        @click="emit('logout')"
      >
        Выйти
      </UButton>
      <UAvatar
        :src="profile.avatar || undefined"
        :alt="fullName"
        class="ring-2 ring-success dark:ring-success shadow-sm size-36 p-1 max-sm:size-24"
      />
      <div class="w-full flex flex-col">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-default">
            {{ fullName }}
          </h1>
          <UButton
            icon="i-heroicons-pencil-square"
            color="neutral"
            variant="link"
            class="justify-center mt-2"
            size="sm"
            to="/settings/account"
          >
            Редактировать
          </UButton>
        </div>
        <ul class="flex font-medium text-muted w-full gap-6">
          <li class="">
            {{ profile.role === "teacher" ? "Преподаватель" : "Студент" }}
          </li>
          <li v-if="profile.student_id" class="list-disc">
            {{ profile.student_id }}
          </li>
          <li v-if="profile.specialization" class="list-disc">
            {{ profile.specialization }}
          </li>
          <li v-if="profile.enrollment_year" class="list-disc">
            {{ profile.enrollment_year }}
          </li>
          <li v-if="profile.experience_years" class="list-disc">
            {{ profile.experience_years }}
          </li>
        </ul>
        <p class="text-sm text-muted mt-1">
          На сайте с {{ formatDate(profile.date_joined) }}
        </p>

        <UCollapsible>
          <button
            class="text-secondary font-semilight text-sm hover:text-secondary/50 cursor-pointer transition-colors"
          >
            Подробнее
          </button>

          <template #content>
            <ProfileInfoDetails :profile="profile" class="mt-2" />
          </template>
        </UCollapsible>
      </div>
    </div>

    <USeparator class="my-6" />
    <div class="flex items-center justify-between w-full gap-2">
      <UButton
        icon="heroicons:academic-cap-16-solid"
        color="primary"
        size="xl"
        class="justify-center"
        to="/dashboard"
      >
        Моё обучение
      </UButton>
    </div>

    <USeparator class="my-6" />
    <h3 class="text-3xl font-bold">О себе</h3>
    <p>
      {{ profile.bio }}
    </p>
  </UCard>
</template>
