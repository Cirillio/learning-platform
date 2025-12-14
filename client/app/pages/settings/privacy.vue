<script lang="ts" setup>
const toast = useToast();

// Privacy settings state
const profileVisibility = ref<"public" | "private" | "students">("students");
const showEmail = ref(false);
const showActivity = ref(true);
const showProgress = ref(true);
const allowMessages = ref(true);
const twoFactorEnabled = ref(false);

// Save handler
const isSaving = ref(false);

const savePreferences = async () => {
  isSaving.value = true;

  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1000));

  toast.add({
    title: "Настройки сохранены",
    description: "Ваши настройки приватности обновлены",
    color: "success",
    icon: "i-lucide-check",
  });

  isSaving.value = false;
};

const visibilityOptions = [
  {
    label: "Публичный",
    value: "public",
    description: "Виден всем пользователям",
  },
  {
    label: "Только студенты",
    value: "students",
    description: "Виден однокурсникам",
  },
  { label: "Приватный", value: "private", description: "Виден только вам" },
];

definePageMeta({
  layout: "settings",
});

useHead({
  title: "Конфиденциальность",
});
</script>

<template>
  <div class="space-y-2 max-w-2xl">
    <!-- Page Header -->
    <div class="pb-2 border-b border-default">
      <h2 class="text-2xl font-bold text-default">Конфиденциальность</h2>
      <p class="text-base text-muted mt-1">
        Управляйте видимостью вашего профиля и данных
      </p>
    </div>

    <!-- Profile Visibility -->
    <UCard :ui="{ body: 'p-3' }">
      <template #header>
        <div class="flex items-center gap-2">
          <div
            class="size-10 rounded-lg bg-primary/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-eye" class="size-5 text-primary" />
          </div>
          <div>
            <h3 class="text-base font-semibold text-default">
              Видимость профиля
            </h3>
            <p class="text-base text-muted">
              Кто может видеть информацию о вас
            </p>
          </div>
        </div>
      </template>

      <URadioGroup
        v-model="profileVisibility"
        :items="visibilityOptions"
        class="space-y-2"
      />
    </UCard>

    <!-- Data Sharing -->
    <UCard :ui="{ body: 'p-3' }">
      <template #header>
        <div class="flex items-center gap-2">
          <div
            class="size-10 rounded-lg bg-info/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-share-2" class="size-5 text-info" />
          </div>
          <div>
            <h3 class="text-base font-semibold text-default">
              Отображение данных
            </h3>
            <p class="text-base text-muted">
              Выберите, какую информацию показывать другим
            </p>
          </div>
        </div>
      </template>

      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-base font-medium text-default">Показывать email</p>
            <p class="text-base text-muted">Ваш email виден в профиле</p>
          </div>
          <USwitch v-model="showEmail" color="info" />
        </div>

        <USeparator />

        <div class="flex items-center justify-between">
          <div>
            <p class="text-base font-medium text-default">
              Показывать активность
            </p>
            <p class="text-base text-muted">Дата последнего входа в систему</p>
          </div>
          <USwitch v-model="showActivity" color="info" />
        </div>

        <USeparator />

        <div class="flex items-center justify-between">
          <div>
            <p class="text-base font-medium text-default">
              Показывать прогресс обучения
            </p>
            <p class="text-base text-muted">Статистика пройденных курсов</p>
          </div>
          <USwitch v-model="showProgress" color="info" />
        </div>
      </div>
    </UCard>

    <!-- Communication -->
    <UCard :ui="{ body: 'p-3' }">
      <template #header>
        <div class="flex items-center gap-2">
          <div
            class="size-10 rounded-lg bg-success/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-message-circle" class="size-5 text-success" />
          </div>
          <div>
            <h3 class="text-base font-semibold text-default">Коммуникации</h3>
            <p class="text-base text-muted">
              Настройки связи с другими пользователями
            </p>
          </div>
        </div>
      </template>

      <div class="flex items-center justify-between">
        <div>
          <p class="text-base font-medium text-default">Разрешить сообщения</p>
          <p class="text-base text-muted">
            Другие пользователи могут писать вам
          </p>
        </div>
        <USwitch v-model="allowMessages" color="success" />
      </div>
    </UCard>

    <!-- Security -->
    <UCard :ui="{ body: 'p-3' }">
      <template #header>
        <div class="flex items-center gap-2">
          <div
            class="size-10 rounded-lg bg-warning/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-shield" class="size-5 text-warning" />
          </div>
          <div>
            <h3 class="text-base font-semibold text-default">Безопасность</h3>
            <p class="text-base text-muted">Дополнительная защита аккаунта</p>
          </div>
        </div>
      </template>

      <div class="flex items-center justify-between">
        <div>
          <p class="text-base font-medium text-default">
            Двухфакторная аутентификация
          </p>
          <p class="text-base text-muted">
            Дополнительный уровень защиты при входе
          </p>
        </div>
        <USwitch v-model="twoFactorEnabled" color="warning" />
      </div>

      <UAlert
        v-if="!twoFactorEnabled"
        color="warning"
        variant="soft"
        icon="i-lucide-alert-triangle"
        title="Рекомендуется включить 2FA"
        description="Двухфакторная аутентификация значительно повышает безопасность вашего аккаунта"
        class="mt-2"
      />
    </UCard>

    <!-- Danger Zone -->
    <UCard class="border-error/30" :ui="{ body: 'p-3' }">
      <template #header>
        <div class="flex items-center gap-2">
          <div
            class="size-10 rounded-lg bg-error/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-trash-2" class="size-5 text-error" />
          </div>
          <div>
            <h3 class="text-base font-semibold text-error">Опасная зона</h3>
            <p class="text-base text-muted">Необратимые действия с аккаунтом</p>
          </div>
        </div>
      </template>

      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-base font-medium text-default">Скачать мои данные</p>
            <p class="text-base text-muted">Экспорт всей вашей информации</p>
          </div>
          <UButton
            color="neutral"
            variant="soft"
            icon="i-lucide-download"
            size="lg"
          >
            Экспорт
          </UButton>
        </div>

        <USeparator />

        <div class="flex items-center justify-between">
          <div>
            <p class="text-base font-medium text-default">Удалить аккаунт</p>
            <p class="text-base text-muted">
              Безвозвратное удаление всех данных
            </p>
          </div>
          <UButton
            color="error"
            variant="soft"
            icon="i-lucide-trash-2"
            size="lg"
          >
            Удалить
          </UButton>
        </div>
      </div>
    </UCard>

    <!-- Save Button -->
    <div class="flex justify-end pt-2">
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
