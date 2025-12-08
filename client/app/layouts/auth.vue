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
  <UMain class="h-dvh">
    <div
      class="w-full min-h-full max-lg:py-12 max-lg:gap-16 flex max-lg:flex-col bg-default max-lg:bg-muted"
    >
      <!-- Logo/Brand -->
      <div
        class="lg:text-start text-center flex items-center lg:items-start flex-col justify-between lg:flex-4/7 w-full lg:p-24"
      >
        <Icon
          name="heroicons:command-line"
          class="lg:size-32 size-16 text-primary animate-pulse"
        />
        <div>
          <h1
            class="lg:text-5xl text-3xl my-2 font-bold text-gray-900 dark:text-white"
          >
            Учебный портал
          </h1>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Образовательная платформа для студентов и преподавателей
          </p>
        </div>
      </div>

      <!-- Auth Form -->
      <div
        class="lg:flex-3/7 lg:border-l-2 border-default w-full flex flex-col max-lg:max-w-2xl lg:bg-muted px-2 sm:px-12 lg:py-24 items-start mx-auto justify-between"
      >
        <slot />
      </div>
    </div>
  </UMain>
</template>
