<script lang="ts" setup>
import type { AvatarProps } from "@nuxt/ui";
import type { User, UserProfile } from "~/types";

const props = defineProps<{
  user: User | null;
}>();
</script>

<template>
  <UButton label="Мои уроки" to="/learning" />
  <USeparator orientation="vertical" color="neutral" class="h-6" />
  <UButton
    to="/profile"
    :label="user?.first_name"
    variant="ghost"
    color="neutral"
  />
</template>
