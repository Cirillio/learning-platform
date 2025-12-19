<script lang="ts" setup>
import type { User } from "~/types";
import type { EditSchema } from "~/components/profile/edit-form.vue";
import { authService } from "~/services";

const authApi = authService();
const {
  data: profile,
  pending: profilePending,
  refresh: refreshProfile, // eslint-disable-line @typescript-eslint/no-unused-vars
} = await useAsyncData<User>("user-profile", () => authApi.fetchUser());

const { patch } = useApi();
const { setUser } = useAuthStore();
const toast = useToast();
const isLoading = ref(false);

async function onSubmit(schema: EditSchema) {
  isLoading.value = true;
  try {
    const newUser = await patch<User>("/auth/profile/", schema);

    setUser(newUser);

    // Обновляем данные в useAsyncData под ключом "user-profile"
    refreshNuxtData("user-profile");

    toast.add({
      title: "Профиль обновлен",
      color: "success",
      icon: "i-lucide-check",
    });
  } catch (error: any) {
    toast.add({
      title: "Ошибка",
      description: error.data?.detail || "Не удалось обновить профиль",
      color: "error",
      icon: "i-lucide-circle-alert",
    });
  } finally {
    isLoading.value = false;
  }
}

useHead({
  title: "Редактирование профиля",
});

definePageMeta({
  layout: "settings",
});
</script>

<template>
  <ProfileEditForm
    class="w-full"
    :profile="profile"
    :onSubmit="onSubmit"
    :isLoading="isLoading"
    :profileLoading="profilePending"
    :error="null"
  />
</template>
