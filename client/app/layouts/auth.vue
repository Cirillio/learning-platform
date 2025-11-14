<script lang="ts" setup>
const authStore = useAuthStore();

// Redirect if already authenticated
onMounted(() => {
  if (authStore.isAuthenticated) {
    navigateTo("/dashboard");
  }
});
</script>

<template>
  <UApp>
    <UMain class="h-dvh">
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

        <!-- Auth Form -->
        <div
          class="flex-3/7 w-full bg-muted flex flex-col px-32 py-24 items-start justify-between"
        >
          <slot />
        </div></div
    ></UMain>
  </UApp>
</template>
