<script setup lang="ts">
interface Props {
  videoUrl: string;
  lessonTitle: string;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  progress: [percent: number];
}>();

const videoContainer = ref<HTMLDivElement | null>(null);
const isFullscreen = ref(false);
const isPlaying = ref(false);
const currentTime = ref(0);
const duration = ref(0);
const volume = ref(1);
const isMuted = ref(false);
const showControls = ref(true);

// Определяем тип видео (YouTube, Vimeo, или прямая ссылка)
const videoType = computed(() => {
  const url = props.videoUrl;
  if (url.includes("youtube.com") || url.includes("youtu.be")) {
    return "youtube";
  }
  if (url.includes("vimeo.com")) {
    return "vimeo";
  }
  return "native";
});

// Извлекаем ID для встраиваемых плееров
const embedId = computed(() => {
  const url = props.videoUrl;

  if (videoType.value === "youtube") {
    // Поддержка разных форматов YouTube URL
    const regExp =
      /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);
    return match?.[2]?.length === 11 ? match[2] : null;
  }

  if (videoType.value === "vimeo") {
    const regExp = /vimeo.*\/(\d+)/i;
    const match = url.match(regExp);
    return match ? match[1] : null;
  }

  return null;
});

const embedUrl = computed(() => {
  if (videoType.value === "youtube" && embedId.value) {
    return `https://www.youtube.com/embed/${embedId.value}?rel=0&modestbranding=1&enablejsapi=1`;
  }
  if (videoType.value === "vimeo" && embedId.value) {
    return `https://player.vimeo.com/video/${embedId.value}?dnt=1`;
  }
  return null;
});

// Отслеживание прогресса просмотра
const progressPercent = computed(() => {
  if (!duration.value) return 0;
  return Math.round((currentTime.value / duration.value) * 100);
});

// Отправляем прогресс каждые 10%
watch(progressPercent, (newPercent, oldPercent) => {
  const newThreshold = Math.floor(newPercent / 10);
  const oldThreshold = Math.floor(oldPercent / 10);

  if (newThreshold > oldThreshold) {
    emit("progress", newPercent);
  }
});

// Форматирование времени
const formatTime = (seconds: number): string => {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, "0")}`;
};

// Для нативного видео
const videoRef = ref<HTMLVideoElement | null>(null);

const handleTimeUpdate = () => {
  if (videoRef.value) {
    currentTime.value = videoRef.value.currentTime;
    duration.value = videoRef.value.duration;
  }
};

const handlePlay = () => {
  isPlaying.value = true;
};

const handlePause = () => {
  isPlaying.value = false;
};

const togglePlay = () => {
  if (!videoRef.value) return;

  if (isPlaying.value) {
    videoRef.value.pause();
  } else {
    videoRef.value.play();
  }
};

const toggleFullscreen = async () => {
  if (!videoContainer.value) return;

  if (!document.fullscreenElement) {
    await videoContainer.value.requestFullscreen();
    isFullscreen.value = true;
  } else {
    await document.exitFullscreen();
    isFullscreen.value = false;
  }
};
</script>

<template>
  <div
    ref="videoContainer"
    class="bg-elevated rounded-xl border border-default overflow-hidden"
  >
    <!-- Video Header -->
    <div class="p-4 border-b border-default flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div
          class="size-10 rounded-lg bg-primary/10 flex items-center justify-center"
        >
          <UIcon name="i-lucide-play-circle" class="size-5 text-primary" />
        </div>
        <div>
          <h3 class="font-medium text-default">Видеоурок</h3>
          <p class="text-sm text-muted">{{ lessonTitle }}</p>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <UButton
          v-if="videoType === 'native'"
          variant="ghost"
          color="neutral"
          icon="i-lucide-maximize"
          size="sm"
          @click="toggleFullscreen"
        />
      </div>
    </div>

    <!-- Video Player -->
    <div class="relative aspect-video bg-neutral">
      <!-- YouTube / Vimeo Embed -->
      <iframe
        v-if="embedUrl"
        :src="embedUrl"
        :title="lessonTitle"
        class="absolute inset-0 w-full h-full"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen
      />

      <!-- Native Video Player -->
      <template v-else-if="videoType === 'native'">
        <video
          ref="videoRef"
          :src="videoUrl"
          class="w-full h-full object-contain"
          @timeupdate="handleTimeUpdate"
          @play="handlePlay"
          @pause="handlePause"
          @loadedmetadata="handleTimeUpdate"
        />

        <!-- Custom Controls Overlay -->
        <div
          v-show="showControls"
          class="absolute inset-0 bg-linear-to-t from-neutral/80 via-transparent to-transparent"
        >
          <!-- Center Play Button -->
          <button
            class="absolute inset-0 flex items-center justify-center group"
            @click="togglePlay"
          >
            <div
              class="size-20 rounded-full bg-primary/90 flex items-center justify-center transition-transform group-hover:scale-110"
            >
              <UIcon
                :name="isPlaying ? 'i-lucide-pause' : 'i-lucide-play'"
                class="size-8 text-white"
                :class="{ 'ml-1': !isPlaying }"
              />
            </div>
          </button>

          <!-- Bottom Controls -->
          <div class="absolute bottom-0 left-0 right-0 p-4 space-y-2">
            <!-- Progress Bar -->
            <div
              class="relative h-1 bg-muted rounded-full overflow-hidden cursor-pointer"
            >
              <div
                class="absolute inset-y-0 left-0 bg-primary rounded-full transition-all"
                :style="{ width: `${progressPercent}%` }"
              />
            </div>

            <!-- Time & Controls -->
            <div class="flex items-center justify-between text-white">
              <span class="text-sm">
                {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
              </span>

              <div class="flex items-center gap-2">
                <UButton
                  variant="ghost"
                  color="neutral"
                  :icon="isMuted ? 'i-lucide-volume-x' : 'i-lucide-volume-2'"
                  size="xs"
                  class="text-white hover:bg-white/20"
                  @click="isMuted = !isMuted"
                />
                <UButton
                  variant="ghost"
                  color="neutral"
                  icon="i-lucide-maximize"
                  size="xs"
                  class="text-white hover:bg-white/20"
                  @click="toggleFullscreen"
                />
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- Fallback: No valid video -->
      <div
        v-else
        class="absolute inset-0 flex flex-col items-center justify-center text-muted"
      >
        <UIcon name="i-lucide-video-off" class="size-12 mb-2" />
        <p>Видео недоступно</p>
      </div>
    </div>
  </div>
</template>
