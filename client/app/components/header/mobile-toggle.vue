<script setup lang="ts">
defineEmits<{
  toggle: [];
}>();
</script>

<template>
  <UButton
    @click="$emit('toggle')"
    variant="outline"
    color="neutral"
    size="xl"
    icon="heroicons:bars-3"
    class="p-3.5 rounded-sm"
  />
</template>