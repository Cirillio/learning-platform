<script lang="ts" setup>
defineEmits<{
  (e: "confirm"): void;
}>();

const open = ref(false);
</script>

<template>
  <UModal
    v-model:open="open"
    :close="false"
    :ui="{
      content: 'group',
      header: 'flex items-start flex-col gap-2',
    }"
  >
    <slot />

    <template #header>
      <div class="relative group-hover:animate-pulse">
        <UIcon class="size-16 text-primary" name="heroicons:academic-cap" />
        <UIcon
          name="heroicons:slash-20-solid"
          class="size-20 text-error absolute top-1/2 left-1/2 -translate-1/2 -translate-x-1/2"
        />
      </div>
      <h3 class="text-3xl font-bold">Отписка от курса</h3>
      <p class="text-base font-semibold text-error">
        Вы уверены, что хотите отписаться? Ваш прогресс будет сохранен, но вы
        потеряете доступ к материалам курса.
      </p>
    </template>

    <template #footer>
      <div class="flex justify-end gap-2 w-full">
        <UButton
          color="neutral"
          variant="soft"
          label="Отмена"
          @click="
            () => {
              open = false;
            }
          "
        />
        <UButton
          color="error"
          variant="subtle"
          label="Отписаться"
          @click="$emit('confirm')"
        />
      </div>
    </template>
  </UModal>
</template>
