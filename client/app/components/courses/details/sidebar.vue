<script setup lang="ts">
import type { CourseDetail } from "~/types";

interface Props {
  course: CourseDetail;
  isUserEnrolled: boolean;
  lessonsCount: number;
}

defineProps<Props>();

defineEmits<{
  (e: "enroll"): void;
}>();
</script>

<template>
  <div class="lg:col-span-1">
    <div class="sticky top-24 space-y-6">
      <!-- Course Action Card -->
      <UCard>
        <!-- Preview Image/Video -->
        <div
          class="relative aspect-video w-full bg-neutral-100 dark:bg-neutral-800 overflow-hidden rounded-t-lg group cursor-pointer"
        >
          <NuxtImg
            v-if="course.cover_image_url"
            :src="course.cover_image_url"
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
          <div
            v-else
            class="w-full h-full flex items-center justify-center text-neutral-400"
          >
            <UIcon name="i-heroicons-photo" class="w-12 h-12" />
          </div>

          <!-- Play Button Overlay -->
          <div
            class="absolute inset-0 flex items-center justify-center bg-black/20 group-hover:bg-black/30 transition-colors"
          >
            <div
              class="w-14 h-14 rounded-full bg-white/90 flex items-center justify-center shadow-lg backdrop-blur-sm transform group-hover:scale-110 transition-all"
            >
              <UIcon
                name="i-heroicons-play-solid"
                class="w-6 h-6 text-primary-600 ml-1"
              />
            </div>
          </div>
          <div
            class="absolute bottom-4 left-0 right-0 text-center text-white text-sm font-medium drop-shadow-md"
          >
            Предпросмотр курса
          </div>
        </div>

        <div class="p-6 space-y-6">
          <!-- Price -->
          <div class="flex items-end gap-2">
            <span class="text-4xl font-bold text-neutral-900 dark:text-white"
              >Бесплатно</span
            >
            <!-- <span class="text-neutral-400 line-through mb-1">5 000 ₽</span> -->
          </div>

          <!-- Actions -->
          <div class="space-y-3">
            <UButton
              v-if="isUserEnrolled"
              block
              size="xl"
              color="success"
              label="Продолжить обучение"
              :to="`/learning/${course.slug}`"
            />
            <UButton
              v-else
              block
              size="xl"
              color="primary"
              label="Записаться на курс"
              :loading="false"
              @click="$emit('enroll')"
            />

            <div class="flex gap-3">
              <UButton
                block
                variant="outline"
                color="neutral"
                class="flex-1"
                label="Купить в подарок"
              />
              <UButton
                icon="i-heroicons-heart"
                color="neutral"
                variant="outline"
                class="aspect-square"
              />
            </div>
          </div>

          <p class="text-xs text-center text-neutral-500">
            Доступ навсегда • Сертификат при завершении
          </p>

          <UDivider />

          <!-- Includes -->
          <div class="space-y-4">
            <h4 class="font-semibold text-sm">Курс включает:</h4>
            <ul
              class="space-y-3 text-sm text-neutral-600 dark:text-neutral-300"
            >
              <li class="flex items-start gap-3">
                <UIcon
                  name="i-heroicons-video-camera"
                  class="w-5 h-5 text-primary-500 shrink-0"
                />
                <span>{{ lessonsCount }} видео-уроков</span>
              </li>
              <li class="flex items-start gap-3">
                <UIcon
                  name="i-heroicons-document-text"
                  class="w-5 h-5 text-primary-500 shrink-0"
                />
                <span
                  >{{ course.assignments_count || 0 }} практических
                  заданий</span
                >
              </li>
              <li class="flex items-start gap-3">
                <UIcon
                  name="i-heroicons-device-phone-mobile"
                  class="w-5 h-5 text-primary-500 shrink-0"
                />
                <span>Доступ с мобильного</span>
              </li>
              <li class="flex items-start gap-3">
                <UIcon
                  name="i-heroicons-academic-cap"
                  class="w-5 h-5 text-primary-500 shrink-0"
                />
                <span>Сертификат об окончании</span>
              </li>
            </ul>
          </div>
        </div>
      </UCard>

      <!-- Calendar Widget (Mockup) -->
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="font-semibold text-sm">Расписание</h3>
            <div class="flex gap-2">
              <UButton
                icon="i-heroicons-chevron-left"
                size="xs"
                color="neutral"
                variant="ghost"
              />
              <span class="text-xs font-medium">Декабрь 2025</span>
              <UButton
                icon="i-heroicons-chevron-right"
                size="xs"
                color="neutral"
                variant="ghost"
              />
            </div>
          </div>
        </template>

        <div
          class="grid grid-cols-7 gap-1 text-center text-xs mb-2 text-neutral-400"
        >
          <span>Пн</span><span>Вт</span><span>Ср</span><span>Чт</span
          ><span>Пт</span><span>Сб</span><span>Вс</span>
        </div>
        <div class="grid grid-cols-7 gap-1 text-center text-sm">
          <span class="text-neutral-300 p-1">29</span>
          <span class="text-neutral-300 p-1">30</span>
          <span class="p-1">1</span>
          <span class="p-1">2</span>
          <span class="p-1">3</span>
          <span class="p-1">4</span>
          <span class="p-1">5</span>
          <span class="p-1">6</span>
          <span class="p-1">7</span>
          <span class="p-1">8</span>
          <span class="p-1">9</span>
          <span class="bg-primary-500 text-white rounded-full p-1 shadow-md"
            >10</span
          >
          <span class="bg-primary-100 text-primary-700 rounded-full p-1"
            >11</span
          >
          <span class="bg-primary-100 text-primary-700 rounded-full p-1"
            >12</span
          >
        </div>
      </UCard>
    </div>
  </div>
</template>
