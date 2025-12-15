<script setup lang="ts">
// Permanent redirect from /dashboard to /learning
definePageMeta({
  middleware: [
    function () {
      return navigateTo("/learning", { redirectCode: 301 });
    },
  ],
});
</script>

<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="text-center">
      <UIcon
        name="i-lucide-loader-2"
        class="size-10 animate-spin text-primary"
      />
      <p class="text-muted mt-2">Перенаправление...</p>
    </div>
  </div>
</template>
