<script setup lang="ts">
import type { CourseDetail } from "~/types";

interface Props {
  course: CourseDetail;
  isUserEnrolled: boolean;
  lessonsCount: number;
  pending: boolean;
}

defineProps<Props>();

defineEmits<{
  (e: "enroll"): void;
  (e: "unenroll"): void;
}>();
</script>

<template>
  <div class="lg:col-span-1">
    <div class="sticky top-14 space-y-6">
      <!-- Course Action Card -->
      <UCard>
        <!-- Preview Image/Video -->
        <div
          class="relative aspect-video w-full bg-neutral-100 dark:bg-neutral-800 overflow-hidden rounded-lg group cursor-pointer"
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

        <div class="py-6 space-y-6">
          <!-- Price -->
          <div
            v-if="!isUserEnrolled"
            class="flex items-center justify-center gap-2"
          >
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
              v-if="isUserEnrolled"
              block
              size="xl"
              color="error"
              variant="subtle"
              label="Отписаться"
              :loading="pending"
              @click="$emit('unenroll')"
            />
            <UButton
              v-else
              block
              size="xl"
              color="primary"
              label="Записаться на курс"
              :loading="pending"
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
            • Сертификат при завершении
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
    </div>
  </div>
</template>
