<script setup lang="ts">
import type { User } from "~/types";

const props = defineProps<{
  profile: User;
}>();

const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return "Не указано";
  return new Date(dateStr).toLocaleDateString("ru-RU");
};

const displayValue = (val: string | number | null | undefined) => {
  return val ? val : "Не указано";
};

const address = computed(() => {
  return (
    [props.profile.country, props.profile.city, props.profile.address]
      .filter(Boolean)
      .join(", ") || "Не указано"
  );
});
</script>

<template>
  <UCard
    :ui="{
      header: 'bg-primary text-white border-0',
    }"
  >
    <template #header>
      <h3 class="font-bold text-2xl">Информация</h3>
    </template>

    <dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-6">
      <div>
        <dt>
          <UBadge size="xl" label="Email" color="secondary" variant="subtle" />
        </dt>
        <dd class="text-lg text-gray-900 dark:text-white">
          {{ displayValue(profile.email) }}
        </dd>
      </div>
      <div>
        <dt>
          <UBadge
            size="xl"
            label="Телефон"
            color="secondary"
            variant="subtle"
          />
        </dt>
        <dd class="text-lg text-gray-900 dark:text-white">
          {{ displayValue(profile.phone) }}
        </dd>
      </div>
      <div>
        <dt>
          <UBadge
            size="xl"
            label="Дата рождения"
            color="secondary"
            variant="subtle"
          />
        </dt>
        <dd class="text-lg text-gray-900 dark:text-white">
          {{ formatDate(profile.birth_date) }}
        </dd>
      </div>
      <div>
        <dt>
          <UBadge
            size="xl"
            label="Специализация"
            color="secondary"
            variant="subtle"
          />
        </dt>

        <dd class="text-lg text-gray-900 dark:text-white">
          {{ displayValue(profile.specialization) }}
        </dd>
      </div>
      <div class="sm:col-span-2">
        <dt>
          <UBadge size="xl" label="Адрес" color="secondary" variant="subtle" />
        </dt>
        <dd class="text-lg text-gray-900 dark:text-white">
          {{ address }}
        </dd>
      </div>
      <div class="sm:col-span-2">
        <dt>
          <UBadge size="xl" label="О себе" color="secondary" variant="subtle" />
        </dt>
        <dd class="text-lg text-gray-900 dark:text-white whitespace-pre-wrap">
          {{ displayValue(profile.bio) }}
        </dd>
      </div>
    </dl>
  </UCard>
</template>
