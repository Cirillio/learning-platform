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
  middleware: "guest",
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
  <div class="w-full flex flex-col max-md:items-center">
    <h2
      class="text-2xl lg:text-3xl font-bold border-b-2 border-primary pb-2 w-fit text-default"
    >
      Авторизация
    </h2>

    <AuthLoginForm :is-loading="authStore.isLoading" @submit="handleLogin" />
  </div>

  <!-- Error message -->
  <div v-if="authStore.error" class="mt-4">
    <UAlert :title="authStore.error" color="error" variant="soft" />
  </div>

  <div class="flex w-fit max-md:mx-auto justify-between items-center mt-4">
    <p class="text-sm text-muted">
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

  <UButton
    label="На главную"
    class="md:hidden mt-24 mx-auto"
    variant="ghost"
    color="neutral"
    leading-icon="heroicons:arrow-left-16-solid"
    to="/"
  />
</template>
