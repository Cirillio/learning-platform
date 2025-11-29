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
    label="Мои доска"
    class="justify-start"
    block
    variant="subtle"
    to="/my/dashboard"
  />

  <UButton
    label="Корзина"
    variant="subtle"
    icon="heroicons:shopping-bag"
    color="secondary"
    block
    class="justify-start"
  />

  <UButton
    label="Уведомления"
    variant="subtle"
    icon="heroicons:bell"
    color="info"
    block
    class="justify-start"
  />
</template>
