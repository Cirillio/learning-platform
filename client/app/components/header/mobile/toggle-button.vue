<script lang="ts" setup>
defineEmits<{
  toggle: [];
}>();
</script>

<template>
  <UButton
    @click="$emit('toggle')"
    variant="outline"
    color="neutral"
    size="md"
    label="Меню"
    icon="heroicons:bars-3"
  />
</template>
