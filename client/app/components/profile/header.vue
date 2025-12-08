<script setup lang="ts">
import type { User } from "~/types";

const props = defineProps<{
  profile: User;
  onEditSuccess: () => Promise<void>;
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
  <UCard class="max-w-xs w-full">
    <div class="flex flex-col items-center gap-6">
      <UAvatar
        :src="profile.avatar || undefined"
        :alt="fullName"
        class="ring-2 ring-success dark:ring-success shadow-sm size-36 p-1 max-sm:size-24"
      />
      <div class="w-full">
        <div class="flex flex-col gap-6 items-center justify-between">
          <div class="w-full flex flex-col text-center">
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ fullName }}
            </h1>
            <p class="text-gray-500 dark:text-gray-400 font-medium">
              {{ profile.role === "teacher" ? "Преподаватель" : "Студент" }}
            </p>
            <p class="text-sm text-gray-400 mt-1">
              На сайте с {{ formatDate(profile.date_joined) }}
            </p>
          </div>
          <div class="flex items-center w-full flex-col gap-2">
            <!-- Edit Modal -->
            <UModal
              :open="isModalOpen"
              :ui="{
                content: 'max-w-3xl',
              }"
            >
              <UButton
                icon="i-heroicons-pencil-square"
                color="neutral"
                variant="subtle"
                size="lg"
                class="justify-center"
                @click="isModalOpen = true"
              >
                Редактировать
              </UButton>
              <template #content>
                <ProfileEditForm
                  v-if="profile"
                  :profile="profile"
                  @cancel="() => (isModalOpen = false)"
                  @success="onEditSuccess"
                />
              </template>
            </UModal>
            <UButton
              trailing-icon="i-heroicons-arrow-right"
              color="error"
              variant="subtle"
              size="lg"
              class="justify-center"
              @click="emit('logout')"
            >
              Выйти
            </UButton>
          </div>
        </div>
      </div>
    </div>
  </UCard>
</template>
