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
  <div class="grid grid-cols-2 grid-rows-2">
    <div class="flex flex-col gap-1">
      <span class="font-semibold text-sm border-b w-fit border-default"
        >Email</span
      >
      <span class="text-muted font-medium">{{
        displayValue(profile.email)
      }}</span>
    </div>
    <div class="flex flex-col gap-1">
      <span class="font-semibold text-sm border-b w-fit border-default"
        >Дата рождения</span
      >
      <span class="text-muted font-medium">{{
        displayValue(formatDate(profile.birth_date))
      }}</span>
    </div>
    <div class="flex flex-col gap-1">
      <span class="font-semibold text-sm border-b w-fit border-default"
        >Телефон</span
      >
      <span class="text-muted font-medium">
        {{ displayValue(profile.phone) }}
      </span>
    </div>
    <div class="flex flex-col gap-1">
      <span class="font-semibold text-sm border-b w-fit border-default"
        >Адрес</span
      >
      <span class="text-muted font-medium"> {{ displayValue(address) }}</span>
    </div>
  </div>
</template>
