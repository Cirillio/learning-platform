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
  <UButton
    to="/my/profile"
    :label="user?.first_name"
    variant="outline"
    color="neutral"
    block
    class="justify-start"
  />

  <UButton
    label="Мои курсы"
    class="justify-start"
    block
    to="/my/dashboard/courses"
  />
</template>
