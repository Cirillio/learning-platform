<script lang="ts" setup>
// Nuxt UI v4 использует v-model:open.
// Мы принимаем стандартный v-model (boolean) от родителя и связываем его с open.
const open = defineModel<boolean>({ default: false });

const { logout, user } = useAuth();
const isLoading = ref(false);

const handleLogout = async () => {
  try {
    isLoading.value = true;
    await logout();
    open.value = false;
    // Hard reload для полной очистки состояния приложения
    window.location.href = "/";
  } catch (error) {
    console.error("Logout error:", error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <UModal
    v-model:open="open"
    title="Выход из системы"
    description="Вы действительно хотите завершить текущую сессию?"
    :dismissible="!isLoading"
    :close="!isLoading"
    @close:prevent="() => (open = false)"
  >
    <template #body>
      <div
        class="flex items-center gap-4 p-3 rounded-lg border border-default bg-(--ui-bg-elevated)/50"
      >
        <UAvatar
          :src="user?.avatar || undefined"
          :alt="user?.username"
          size="md"
        />
        <div class="min-w-0 flex-1">
          <p class="text-sm font-medium text-highlighted truncate">
            {{ user?.first_name }} {{ user?.last_name }}
          </p>
          <p class="text-xs text-muted truncate">
            {{ user?.username }}
          </p>
        </div>
        <UBadge
          :label="user?.role === 'teacher' ? 'Преподаватель' : 'Студент'"
          :color="user?.role === 'teacher' ? 'primary' : 'neutral'"
          variant="subtle"
          size="sm"
        />
      </div>
    </template>

    <slot />

    <template #footer>
      <div class="flex justify-end gap-2 w-full">
        <UButton
          label="Отмена"
          color="neutral"
          variant="ghost"
          :disabled="isLoading"
          @click="open = false"
        />

        <UButton
          label="Выйти"
          color="error"
          variant="subtle"
          icon="i-lucide-log-out"
          :loading="isLoading"
          @click="handleLogout"
        />
      </div>
    </template>
  </UModal>
</template>
