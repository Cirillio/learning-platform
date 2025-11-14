<script setup lang="ts">
import type { LoginForm } from "~/schemas/auth.schema";

const { login } = useAuth();
const authStore = useAuthStore();

// Redirect if already authenticated
onMounted(() => {
  if (authStore.isAuthenticated) {
    navigateTo("/dashboard");
  }
});

// Handle login
const handleLogin = async (credentials: LoginForm): Promise<void> => {
  try {
    await login(credentials);
  } catch (error: any) {
    authStore.setError(error.data?.message || error.message || "Ошибка входа");
  }
};

// Handle register navigation
const handleRegister = (): void => {
  navigateTo("/auth/register");
};

// Meta
definePageMeta({
  layout: false,
});

// SEO
useHead({
  title: "Вход в систему",
  meta: [{ name: "description", content: "Вход в систему учебного портала" }],
});
</script>

<template>
  <div class="min-h-screen flex h-full items-stretch">
    <div
      class="fixed top-0 left-0 right-0 flex justify-start gap-4 items-center w-full py-4 px-24"
    >
      <UButton
        leading-icon="heroicons:arrow-left"
        label="На главную"
        class="px-2.5 py-1 text-lg"
        variant="subtle"
        color="secondary"
        size="lg"
      />
      <UColorModeButton
        variant="subtle"
        class="size-9 *:size-6 grid place-items-center"
      />
    </div>
    <div class="w-full min-h-full flex">
      <!-- Logo/Brand -->
      <div
        class="text-center flex items-start flex-col justify-center flex-4/7 w-full p-24"
      >
        <Icon name="heroicons:command-line" class="size-24 text-primary" />
        <h1 class="text-5xl mt-4 font-bold text-gray-900 dark:text-white">
          Учебный портал
        </h1>
        <p class="text-lg text-gray-600 dark:text-gray-400">
          Образовательная платформа для студентов и преподавателей
        </p>
      </div>

      <!-- Login Form -->
      <div
        class="flex-3/7 w-full bg-muted flex flex-col px-32 p-12 items-start justify-between"
      >
        <h2 class="text-2xl font-semibold">Добро пожаловать!</h2>
        <div class="w-full">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Авторизация</h2>

          <AuthLoginForm
            :is-loading="authStore.isLoading"
            @submit="handleLogin"
            @register="handleRegister"
          />
        </div>

        <!-- Error message -->
        <div v-if="authStore.error" class="mt-4">
          <UAlert :title="authStore.error" color="error" variant="soft" />
        </div>

        <div>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Нет аккаунта?
            <UButton variant="link" color="info" class="p-0 h-auto font-medium">
              Зарегистрироваться
            </UButton>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
