<script lang="ts" setup>
import type { AvatarProps } from "@nuxt/ui";
import type { User } from "~/types";

const props = defineProps<{
  user: User | null;
}>();

const emit = defineEmits<{
  openFeedback: [];
}>();

const avatarProps = computed<AvatarProps | undefined>(() => {
  const avatar = props.user?.avatar;
  return avatar
    ? { src: avatar, alt: props.user?.first_name ?? "avatar" }
    : undefined;
});

// Динамические ссылки в зависимости от роли
const isTeacher = computed(() => props.user?.role === "teacher");
const profileLink = computed(() =>
  isTeacher.value ? "/teacher/profile" : "/profile"
);
const dashboardLink = computed(() =>
  isTeacher.value ? "/teacher" : "/learning"
);
const dashboardLabel = computed(() =>
  isTeacher.value ? "Панель учителя" : "Мои курсы"
);
</script>

<template>
  <UButton
    :to="profileLink"
    icon="heroicons:user"
    :label="user?.first_name"
    variant="outline"
    color="neutral"
    block
    class="justify-start"
  />

  <USeparator />

  <UButton
    icon="heroicons:academic-cap"
    :label="dashboardLabel"
    class="justify-start"
    block
    variant="subtle"
    :to="dashboardLink"
  />

  <UButton
    label="Настройки"
    variant="subtle"
    icon="heroicons:cog-6-tooth"
    color="neutral"
    block
    class="justify-start"
    to="/settings"
  />

  <UButton
    label="Уведомления"
    variant="subtle"
    icon="heroicons:bell"
    color="info"
    block
    class="justify-start"
    to="/settings/notifications"
  />

  <UButton
    label="Обратная связь"
    variant="subtle"
    icon="heroicons:chat-bubble-left-right"
    color="neutral"
    block
    class="justify-start"
    @click="emit('openFeedback')"
  />
</template>
