<script setup lang="ts">
defineProps<{
  videoUrl: string;
}>();
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center gap-2">
        <UIcon name="i-lucide-video" class="size-5 text-primary" />
        <h3 class="font-semibold">Видео урока</h3>
      </div>
    </template>
    <div class="aspect-video rounded-lg overflow-hidden bg-elevated">
      <iframe
        v-if="videoUrl.includes('youtube')"
        :src="videoUrl.replace('watch?v=', 'embed/')"
        class="w-full h-full"
        frameborder="0"
        allowfullscreen
      />
      <video
        v-else
        :src="videoUrl"
        controls
        class="w-full h-full"
      />
    </div>
  </UCard>
</template>
