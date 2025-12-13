<script setup lang="ts">
import type { User } from "~/types";

const props = defineProps<{
  user: User | null;
}>();

const emit = defineEmits<{
  (e: "logout"): void;
}>();

const fullName = computed(() => {
  return (
    `${props.user?.first_name || ""} ${props.user?.last_name || ""}`.trim() ||
    props.user?.username
  );
});

const formatDate = (date: string | null | undefined): string => {
  if (!date) return "Не указано";
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(new Date(date));
};
</script>

<template>
  <UCard>
    <div class="flex flex-col md:flex-row gap-2">
      <!-- Avatar -->
      <div class="flex flex-col items-center gap-2">
        <UAvatar
          :src="user?.avatar || undefined"
          :alt="fullName"
          class="ring-2 ring-primary/50 text-2xl size-24"
        />
        <UBadge color="primary" variant="subtle" size="xl" class="mt-auto">
          <UIcon name="i-lucide-graduation-cap" class="size-4" />
          Преподаватель
        </UBadge>
      </div>

      <!-- Info -->
      <div class="flex-1">
        <div class="flex items-start justify-between gap-2 mb-4">
          <div>
            <h1 class="text-2xl font-bold text-default">{{ fullName }}</h1>
            <p class="text-muted">@{{ user?.username }}</p>
          </div>
          <div class="flex items-center gap-2">
            <UButton
              icon="i-lucide-pencil"
              color="neutral"
              variant="soft"
              @click="navigateTo('/settings/account')"
            >
              Редактировать
            </UButton>
          </div>
        </div>

        <div class="space-y-2">
          <div
            v-if="user?.specialization"
            class="flex items-center gap-2 text-muted"
          >
            <UIcon name="i-lucide-briefcase" class="size-4" />
            <span>{{ user.specialization }}</span>
          </div>
          <div v-if="user?.bio" class="text-default">
            {{ user.bio }}
          </div>
          <div class="flex items-center gap-2 text-sm text-muted">
            <UIcon name="i-lucide-calendar" class="size-4" />
            <span>На платформе с {{ formatDate(user?.date_joined) }}</span>
          </div>
        </div>
      </div>
    </div>
  </UCard>
</template>
