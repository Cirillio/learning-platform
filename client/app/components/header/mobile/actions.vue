<script lang="ts" setup>
import { getHeaderMenuItems } from "~/constants/header-config";

const props = defineProps<{
  onLogout: () => void;
}>();

const { headerMenuItems } = getHeaderMenuItems({
  onLogout: props.onLogout,
});
</script>

<template>
  <div class="flex gap-1 flex-col">
    <UButton
      v-for="item in headerMenuItems"
      :key="item.label"
      :icon="item.icon"
      :label="item.label"
      :color="item.color"
      :variant="item.variant"
      :to="item.to"
      @click="item.onClick"
    />
  </div>
</template>
