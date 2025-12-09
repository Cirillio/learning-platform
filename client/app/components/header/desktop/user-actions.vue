<script lang="ts" setup>
import type { AvatarProps } from "@nuxt/ui";
import type { User } from "~/types";

const props = defineProps<{
  user: User | null;
}>();

const avatarProps = computed<AvatarProps | undefined>(() => {
  const avatar = props.user?.avatar;
  return avatar
    ? { src: avatar, alt: props.user?.first_name ?? "avatar" }
    : undefined;
});
</script>

<template>
  <UButton label="Моя доска" to="/dashboard" />
  <USeparator orientation="vertical" color="neutral" class="h-6" />
  <UButton
    to="/my/profile"
    :label="user?.first_name"
    variant="ghost"
    color="neutral"
  />
</template>
