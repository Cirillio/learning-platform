<script lang="ts" setup>
const toast = useToast();

// Notification preferences state
const emailNotifications = ref(true);
const pushNotifications = ref(false);
const courseUpdates = ref(true);
const assignmentReminders = ref(true);
const gradeNotifications = ref(true);
const promotionalEmails = ref(false);
const weeklyDigest = ref(true);

// Save handler
const isSaving = ref(false);

const savePreferences = async () => {
  isSaving.value = true;

  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1000));

  toast.add({
    title: "Настройки сохранены",
    description: "Ваши предпочтения уведомлений обновлены",
    color: "success",
    icon: "i-lucide-check",
  });

  isSaving.value = false;
};

definePageMeta({
  layout: "settings",
});

useHead({
  title: "Уведомления",
});
</script>

<template>
  <div class="space-y-6 max-w-2xl">
    <!-- Page Header -->
    <div class="pb-4 border-b border-default">
      <h2 class="text-xl font-semibold text-default">Настройки уведомлений</h2>
      <p class="text-sm text-muted mt-1">
        Управляйте способами получения уведомлений
      </p>
    </div>

    <!-- Email Notifications -->
    <UCard>
      <template #header>
        <div class="flex items-center gap-3">
          <div
            class="size-10 rounded-lg bg-primary/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-mail" class="size-5 text-primary" />
          </div>
          <div>
            <h3 class="font-semibold text-default">Email-уведомления</h3>
            <p class="text-sm text-muted">
              Получайте уведомления на вашу почту
            </p>
          </div>
        </div>
      </template>

      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium text-default">Включить email-уведомления</p>
            <p class="text-sm text-muted">
              Основной переключатель для всех email
            </p>
          </div>
          <USwitch v-model="emailNotifications" color="primary" />
        </div>

        <USeparator />

        <div
          class="space-y-4 transition-opacity"
          :class="{ 'opacity-50 pointer-events-none': !emailNotifications }"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-default">Обновления курсов</p>
              <p class="text-sm text-muted">
                Новые уроки, материалы и объявления
              </p>
            </div>
            <USwitch v-model="courseUpdates" color="primary" />
          </div>

          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-default">Напоминания о заданиях</p>
              <p class="text-sm text-muted">
                Сроки сдачи и непроверенные работы
              </p>
            </div>
            <USwitch v-model="assignmentReminders" color="primary" />
          </div>

          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-default">Уведомления об оценках</p>
              <p class="text-sm text-muted">
                Новые оценки и комментарии преподавателей
              </p>
            </div>
            <USwitch v-model="gradeNotifications" color="primary" />
          </div>

          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-default">Еженедельный дайджест</p>
              <p class="text-sm text-muted">Сводка активности за неделю</p>
            </div>
            <USwitch v-model="weeklyDigest" color="primary" />
          </div>
        </div>
      </div>
    </UCard>

    <!-- Push Notifications -->
    <UCard>
      <template #header>
        <div class="flex items-center gap-3">
          <div
            class="size-10 rounded-lg bg-warning/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-bell" class="size-5 text-warning" />
          </div>
          <div>
            <h3 class="font-semibold text-default">Push-уведомления</h3>
            <p class="text-sm text-muted">Мгновенные уведомления в браузере</p>
          </div>
        </div>
      </template>

      <div class="flex items-center justify-between">
        <div>
          <p class="font-medium text-default">Включить push-уведомления</p>
          <p class="text-sm text-muted">Требуется разрешение браузера</p>
        </div>
        <USwitch v-model="pushNotifications" color="warning" />
      </div>

      <UAlert
        v-if="!pushNotifications"
        color="neutral"
        variant="soft"
        icon="i-lucide-info"
        title="Push-уведомления отключены"
        description="Включите для получения мгновенных оповещений о важных событиях"
        class="mt-4"
      />
    </UCard>

    <!-- Marketing -->
    <UCard>
      <template #header>
        <div class="flex items-center gap-3">
          <div
            class="size-10 rounded-lg bg-info/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-megaphone" class="size-5 text-info" />
          </div>
          <div>
            <h3 class="font-semibold text-default">Маркетинговые рассылки</h3>
            <p class="text-sm text-muted">
              Новости, акции и специальные предложения
            </p>
          </div>
        </div>
      </template>

      <div class="flex items-center justify-between">
        <div>
          <p class="font-medium text-default">Получать промо-материалы</p>
          <p class="text-sm text-muted">Информация о новых курсах и скидках</p>
        </div>
        <USwitch v-model="promotionalEmails" color="info" />
      </div>
    </UCard>

    <!-- Save Button -->
    <div class="flex justify-end pt-4">
      <UButton
        color="primary"
        size="lg"
        :loading="isSaving"
        icon="i-lucide-save"
        @click="savePreferences"
      >
        Сохранить настройки
      </UButton>
    </div>
  </div>
</template>
