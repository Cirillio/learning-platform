<script setup lang="ts">
import type { RegisterForm } from "~/schemas/auth.schema";

const { register } = useAuth();
const authStore = useAuthStore();

// Handle register
const handleRegister = async (userData: RegisterForm): Promise<void> => {
  try {
    await register(userData);
  } catch (error: any) {
    authStore.setError(error.data?.message || error.message || "Ошибка регистрации");
  }
};

// Meta
definePageMeta({
  layout: "auth",
});

// SEO
useHead({
  title: "Регистрация",
  meta: [{ name: "description", content: "Регистрация в учебном портале" }],
});
</script>

<template>
  <div class="flex gap-4">
    <UButton
      leading-icon="heroicons:arrow-left"
      variant="ghost"
      color="neutral"
      size="lg"
      to="/"
    />

    <h2 class="text-2xl font-semibold">Добро пожаловать!</h2>
  </div>
  <div class="w-full">
    <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Регистрация</h2>

    <AuthRegisterForm :is-loading="authStore.isLoading" @submit="handleRegister" />
  </div>

  <!-- Error message -->
  <div v-if="authStore.error" class="mt-4">
    <UAlert :title="authStore.error" color="error" variant="soft" />
  </div>

  <div class="flex w-full justify-between items-center">
    <p class="text-sm text-gray-600 dark:text-gray-400">
      Уже есть аккаунт?
      <UButton
        variant="link"
        color="info"
        class="p-0 h-auto font-medium"
        to="/auth/login"
      >
        Войти
      </UButton>
    </p>
    <UColorModeButton variant="subtle" class="size-8 *:size-5 grid place-items-center" />
  </div>
</template>
