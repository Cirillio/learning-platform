<script setup lang="ts">
import type { CourseDetail } from "~/types";

interface Props {
  course: CourseDetail;
  breadcrumbs: { label: string; to: string }[];
}

defineProps<Props>();

const upcomingDate = new Date().toLocaleDateString("ru-RU", {
  day: "numeric",
  month: "long",
  year: "numeric",
});
</script>

<template>
  <div class="bg-black text-white pt-8 pb-24 relative overflow-hidden">
    <!-- Background decoration (optional) -->
    <div
      class="absolute top-0 right-0 w-full h-full bg-linear-to-r dark:from-default to-primary/75 pointer-events-none"
    ></div>

    <UContainer>
      <!-- Breadcrumbs -->
      <UBreadcrumb :links="breadcrumbs" class="mb-6" />

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 relative z-10">
        <!-- Left Column: Course Info -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Category Badge -->
          <UBadge
            v-if="course.category"
            color="primary"
            variant="subtle"
            class="mb-2"
          >
            {{ course.category.name }}
          </UBadge>

          <!-- Title -->
          <h1 class="text-3xl md:text-4xl lg:text-5xl font-bold leading-tight">
            {{ course.title }}
          </h1>

          <!-- Metadata Row -->
          <div
            class="flex flex-wrap items-center gap-6 text-sm text-neutral-300"
          >
            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-users" class="w-5 h-5" />
              <span>{{ course.enrolled_count }} студентов</span>
            </div>
            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-language" class="w-5 h-5" />
              <span>Русский</span>
            </div>
            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-signal" class="w-5 h-5" />
              <span class="capitalize">{{ course.difficulty }}</span>
            </div>
          </div>

          <!-- Short Description -->
          <p class="text-lg text-neutral-300 leading-relaxed max-w-2xl">
            {{ course.short_description }}
          </p>

          <!-- Date & Payment (Mockup style) -->
          <div
            class="pt-4 border-t border-neutral-700 flex flex-col sm:flex-row gap-6 sm:items-center"
          >
            <div>
              <span
                class="text-neutral-400 text-xs uppercase tracking-wider block mb-1"
                >Дата начала</span
              >
              <span class="font-medium text-primary-400">{{
                upcomingDate
              }}</span>
            </div>
            <!-- Payment Icons (Visual only) -->
            <div
              class="flex gap-2 opacity-70 grayscale hover:grayscale-0 transition-all"
            >
              <div
                class="h-6 w-10 bg-neutral-700 rounded flex items-center justify-center text-[10px]"
              >
                VISA
              </div>
              <div
                class="h-6 w-10 bg-neutral-700 rounded flex items-center justify-center text-[10px]"
              >
                MC
              </div>
            </div>
          </div>
        </div>
      </div>
    </UContainer>
  </div>
</template>
