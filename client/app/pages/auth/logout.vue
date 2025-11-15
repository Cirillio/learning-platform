<script setup lang="ts">
const { logout, user, isAuthenticated } = useAuth();

// Handle logout confirmation
const handleLogout = async (): Promise<void> => {
  await logout();
};

// Handle cancel - go back
const handleCancel = (): void => {
  if (process.client) {
    window.history.back();
  } else {
    navigateTo("/");
  }
};

onMounted(() => {
  if (!isAuthenticated) {
    navigateTo("/");
  }
});

// Meta
definePageMeta({
  layout: false,
});

// SEO
useHead({
  title: "Выход из системы",
  meta: [{ name: "description", content: "Подтверждение выхода из системы" }],
});
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <UPageCard
      :ui="{
        wrapper: 'items-stretch',
      }"
    >
      <template #header>
        <div class="flex flex-col gap-2 items-center">
          <UIcon name="i-heroicons-arrow-right-on-rectangle" class="size-8 text-error" />
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
            Выход из системы
          </h1>
          <p class="text-gray-600 dark:text-gray-300">Подтверждение выхода из системы</p>
        </div>
      </template>
      <template #body>
        <!-- User Info -->
        <UCard class="mt-8 mb-8">
          <div class="flex items-center gap-4">
            <UAvatar
              :src="user?.profile?.avatar"
              :alt="`${user?.first_name} ${user?.last_name}`"
              size="xl"
              class="text-primary"
            >
              <UIcon name="i-heroicons-user" class="w-6 h-6" />
            </UAvatar>

            <div class="flex-1 min-w-0">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                {{ user?.first_name }} {{ user?.last_name }}
              </h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ user?.username }}
              </p>
              <UBadge
                :color="user?.role === 'teacher' ? 'primary' : 'secondary'"
                variant="outline"
                class="mt-2"
                size="sm"
              >
                {{ user?.role === "teacher" ? "Преподаватель" : "Студент" }}
              </UBadge>
            </div>
          </div>
        </UCard>

        <!-- Action Buttons -->
        <div class="space-y-3">
          <UButton
            color="secondary"
            size="lg"
            class="text-base"
            block
            @click="handleCancel"
          >
            <template #leading>
              <UIcon class="size-5" name="i-heroicons-arrow-left" />
            </template>
            Отмена
          </UButton>
          <UButton
            color="error"
            variant="soft"
            size="lg"
            class="text-base"
            block
            @click="handleLogout"
          >
            <template #leading>
              <UIcon class="size-5" name="i-heroicons-arrow-right-on-rectangle" />
            </template>
            Выйти из системы
          </UButton>
        </div>
      </template>

      <template #footer>
        <p class="text-sm text-gray-500 dark:text-gray-400 text-center">
          Вы всегда сможете войти снова
        </p>
      </template>
    </UPageCard>
  </div>
</template>
