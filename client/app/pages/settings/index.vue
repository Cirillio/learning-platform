<script lang="ts" setup>
import { authService } from "~/services";
import type { User } from "~/types";

const authApi = authService();
const { user } = useAuthStore();
const toast = useToast();

// Theme settings
const colorMode = useColorMode();
const themeOptions = [
  { label: "Светлая", value: "light", icon: "i-lucide-sun" },
  { label: "Тёмная", value: "dark", icon: "i-lucide-moon" },
  { label: "Системная", value: "system", icon: "i-lucide-monitor" },
];

const currentTheme = computed({
  get: () => colorMode.preference,
  set: (val) => {
    colorMode.preference = val;
  },
});

// Language settings (placeholder)
const languageOptions = [
  { label: "Русский", value: "ru" },
  { label: "English", value: "en" },
];
const currentLanguage = ref("ru");

definePageMeta({
  layout: "settings",
});

useHead({
  title: "Общие настройки",
});
</script>

<template>
  <div class="space-y-2 max-w-2xl">
    <!-- Page Header -->
    <div class="pb-2 border-b border-default">
      <h2 class="text-2xl font-bold text-default">Общие настройки</h2>
      <p class="text-base text-muted mt-1">
        Настройте внешний вид и язык интерфейса
      </p>
    </div>

    <!-- Theme Section -->
    <UCard :ui="{ body: 'p-3' }">
      <template #header>
        <div class="flex items-center gap-2">
          <div
            class="size-10 rounded-lg bg-primary/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-palette" class="size-5 text-primary" />
          </div>
          <div>
            <h3 class="text-base font-semibold text-default">
              Тема оформления
            </h3>
            <p class="text-base text-muted">
              Выберите предпочитаемую цветовую схему
            </p>
          </div>
        </div>
      </template>

      <div class="grid grid-cols-3 gap-2">
        <button
          v-for="theme in themeOptions"
          :key="theme.value"
          class="flex flex-col items-center gap-2 p-3 rounded-xl border-2 transition-all"
          :class="[
            currentTheme === theme.value
              ? 'border-primary bg-primary/5'
              : 'border-default hover:border-primary/50',
          ]"
          @click="currentTheme = theme.value"
        >
          <UIcon :name="theme.icon" class="size-6 text-muted" />
          <span class="text-base font-medium text-default">{{
            theme.label
          }}</span>
        </button>
      </div>
    </UCard>

    <!-- Language Section -->
    <UCard :ui="{ body: 'p-3' }">
      <template #header>
        <div class="flex items-center gap-2">
          <div
            class="size-10 rounded-lg bg-info/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-globe" class="size-5 text-info" />
          </div>
          <div>
            <h3 class="text-base font-semibold text-default">
              Язык интерфейса
            </h3>
            <p class="text-base text-muted">Выберите язык отображения</p>
          </div>
        </div>
      </template>

      <USelect
        v-model="currentLanguage"
        :items="languageOptions"
        placeholder="Выберите язык"
        class="max-w-xs"
        size="lg"
      />

      <UAlert
        color="info"
        variant="soft"
        icon="i-lucide-info"
        title="В разработке"
        description="Поддержка других языков будет добавлена в ближайшее время"
        class="mt-2"
      />
    </UCard>

    <!-- Account Info -->
    <UCard :ui="{ body: 'p-3' }">
      <template #header>
        <div class="flex items-center gap-2">
          <div
            class="size-10 rounded-lg bg-success/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-user-circle" class="size-5 text-success" />
          </div>
          <div>
            <h3 class="text-base font-semibold text-default">
              Информация об аккаунте
            </h3>
            <p class="text-base text-muted">Основные данные вашего профиля</p>
          </div>
        </div>
      </template>

      <div class="space-y-2">
        <div
          class="flex items-center justify-between py-2 border-b border-default"
        >
          <span class="text-base text-muted">Email</span>
          <span class="text-base text-default font-medium">{{
            user?.email || "—"
          }}</span>
        </div>
        <div
          class="flex items-center justify-between py-2 border-b border-default"
        >
          <span class="text-base text-muted">Имя пользователя</span>
          <span class="text-base text-default font-medium">{{
            user?.username || "—"
          }}</span>
        </div>
        <div
          class="flex items-center justify-between py-2 border-b border-default"
        >
          <span class="text-base text-muted">Роль</span>
          <UBadge
            :color="user?.role === 'teacher' ? 'primary' : 'secondary'"
            variant="soft"
          >
            {{ user?.role === "teacher" ? "Преподаватель" : "Студент" }}
          </UBadge>
        </div>
        <div class="flex items-center justify-between py-2">
          <span class="text-base text-muted">Дата регистрации</span>
          <span class="text-base text-default font-medium">
            {{
              user?.date_joined
                ? new Date(user.date_joined).toLocaleDateString("ru-RU")
                : "—"
            }}
          </span>
        </div>
      </div>

      <template #footer>
        <UButton
          to="/settings/account"
          color="primary"
          variant="soft"
          trailing-icon="i-lucide-arrow-right"
          size="lg"
        >
          Редактировать профиль
        </UButton>
      </template>
    </UCard>
  </div>
</template>
