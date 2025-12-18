<script lang="ts" setup>
import { getHeaderMenuItems } from "~/constants/header-config";

const logoutDialogOpen = ref(false);
const feedbackDialogOpen = ref(false);

const { headerMenuItems } = getHeaderMenuItems({
  onLogout: () => {
    logoutDialogOpen.value = true;
  },
  onFeedback: () => {
    feedbackDialogOpen.value = true;
  },
});
</script>

<template>
  <UPopover
    :content="{
      align: 'end',
      sideOffset: 8,
    }"
    :ui="{
      content: '!bg-default/90 backdrop-filter-md',
    }"
  >
    <UButton
      icon="heroicons:ellipsis-vertical-16-solid"
      variant="ghost"
      color="neutral"
    />

    <template #content>
      <div class="flex flex-col gap-2 p-2">
        <USeparator />
        <UButton
          v-for="item in headerMenuItems"
          :key="item.label"
          v-bind="item"
          class="justify-center"
        />
        <USeparator />
      </div>
    </template>
  </UPopover>

  <AuthLogoutDialog v-model="logoutDialogOpen" />
  <FeedbackDialog v-model="feedbackDialogOpen" />
</template>
