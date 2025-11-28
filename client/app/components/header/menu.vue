<script lang="ts" setup>
import { getHeaderMenuItems } from "~/constants/header-config";

const logoutDialogOpen = ref(false);

const { headerMenuItems } = getHeaderMenuItems({
  onLogout: () => {
    logoutDialogOpen.value = true;
  },
});
</script>

<template>
  <UPopover
    :content="{
      align: 'end',
      sideOffset: 8,
    }"
  >
    <UButton
      icon="heroicons:ellipsis-vertical-16-solid"
      variant="ghost"
      color="neutral"
    />

    <template #content>
      <div class="flex flex-col gap-1 p-1">
        <UButton
          v-for="item in headerMenuItems"
          :key="item.label"
          v-bind="item"
          class="justify-center"
        />
      </div>
    </template>
  </UPopover>
  <AuthLogoutDialog v-model="logoutDialogOpen" />
</template>
