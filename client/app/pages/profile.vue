<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-6">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            Dashboard
          </h1>
          <UButton
            color="error"
            variant="outline"
            @click="handleLogout"
            :loading="isLoading"
          >
            Выйти
          </UButton>
        </div>

        <div v-if="user" class="space-y-4">
          <div class="flex items-center space-x-4">
            <UAvatar
              :text="userInitials"
              size="xl"
              class="bg-primary-500"
            />
            <div>
              <h2 class="text-2xl font-semibold text-gray-900 dark:text-white">
                {{ user.first_name }} {{ user.last_name }}
              </h2>
              <p class="text-gray-600 dark:text-gray-400">@{{ user.username }}</p>
            </div>
          </div>

          <UDivider />

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
              <p class="text-sm text-gray-600 dark:text-gray-400">Email</p>
              <p class="text-lg font-medium text-gray-900 dark:text-white">
                {{ user.email }}
              </p>
            </div>

            <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
              <p class="text-sm text-gray-600 dark:text-gray-400">Роль</p>
              <p class="text-lg font-medium text-gray-900 dark:text-white capitalize">
                {{ user.role }}
              </p>
            </div>

            <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
              <p class="text-sm text-gray-600 dark:text-gray-400">Дата регистрации</p>
              <p class="text-lg font-medium text-gray-900 dark:text-white">
                {{ formatDate(user.date_joined) }}
              </p>
            </div>

            <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
              <p class="text-sm text-gray-600 dark:text-gray-400">Статус</p>
              <UBadge
                :color="user.is_active ? 'success' : 'error'"
                variant="subtle"
                size="lg"
              >
                {{ user.is_active ? 'Активен' : 'Неактивен' }}
              </UBadge>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-8">
          <p class="text-gray-600 dark:text-gray-400">Загрузка профиля...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ['auth'],
  layout: 'default',
});

const { user, logout, isLoading } = useAuth();

const userInitials = computed(() => {
  if (!user) return '';
  const first = user.first_name?.[0] || '';
  const last = user.last_name?.[0] || '';
  return `${first}${last}`.toUpperCase();
});

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

async function handleLogout(): Promise<void> {
  await logout();
}
</script>
