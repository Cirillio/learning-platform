<script setup lang="ts">
import type { LoginForm } from "~/schemas/auth.schema";

const { login } = useAuth();
const authStore = useAuthStore();

// Handle login
const handleLogin = async (credentials: LoginForm): Promise<void> => {
  try {
    await login(credentials);
  } catch (error: any) {
    authStore.setError(error.data?.message || error.message || "Ошибка входа");
  }
};

// Meta
definePageMeta({
  layout: "auth",
});

// SEO
useHead({
  title: "Вход в систему",
  meta: [{ name: "description", content: "Вход в систему учебного портала" }],
});
</script>

<template>
  <div class="flex gap-4 max-lg:hidden">
    <UButton
      leading-icon="heroicons:arrow-left"
      variant="ghost"
      color="neutral"
      size="lg"
      to="/"
    />

    <h2 class="text-2xl font-semibold">С возвращением!</h2>
  </div>
  <div class="w-full">
    <h2
      class="text-3xl font-bold border-b-2 border-primary pb-2 w-fit text-gray-900 dark:text-white"
    >
      Авторизация
    </h2>

    <AuthLoginForm :is-loading="authStore.isLoading" @submit="handleLogin" />
  </div>

  <!-- Error message -->
  <div v-if="authStore.error" class="mt-4">
    <UAlert :title="authStore.error" color="error" variant="soft" />
  </div>

  <div class="flex w-full justify-between items-center">
    <p class="text-sm text-gray-600 dark:text-gray-400">
      Нет аккаунта?
      <UButton
        variant="link"
        color="info"
        class="p-0 h-auto font-medium"
        to="/auth/register"
      >
        Зарегистрироваться
      </UButton>
    </p>
  </div>
</template>
