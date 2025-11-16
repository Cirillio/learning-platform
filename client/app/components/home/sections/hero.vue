<script setup lang="ts">
import type { ButtonProps } from "@nuxt/ui";

// SEO мета-теги для Hero секции
useSeoMeta({
  title: "Главная - Учебный портал",
  description:
    "Современная платформа для обучения и взаимодействия студентов и преподавателей",
  ogImage: "/hello-pic.png",
  ogType: "website",
});

const { isAuthenticated } = useAuth();

// Данные для кнопок (SSR-safe: без функций)
const heroLinks = computed<ButtonProps[]>(() =>
  !isAuthenticated
    ? [
        {
          label: "Начать обучение",
          to: "/auth/register",
          color: "primary" as const,
          variant: "solid" as const,
          size: "xl" as const,
          class: "group/btn text-xl",
        },
        {
          label: "Посмотреть курсы",
          to: "/courses",
          color: "secondary" as const,
          variant: "subtle" as const,
          size: "xl" as const,
          class: "group/btn  text-xl",
        },
      ]
    : [
        {
          label: "Мои курсы",
          to: "/dashboard/courses",
          color: "primary" as const,
          size: "xl" as const,
          variant: "solid" as const,
          trailingIcon: "i-heroicons-arrow-right",
          class: "group/btn text-xl",
        },
      ]
);

// Анимационные состояния
const imageLoaded = ref(false);

// Обработчик загрузки изображения
const onImageLoad = () => {
  imageLoaded.value = true;
};

const stats = ref([
  { label: "Категорий", value: 8 },
  { label: "Курсов", value: 120 },
  { label: "Студентов", value: 3500 },
  { label: "Преподавателей", value: 85 },
]);
</script>

<template>
  <section class="relative h-dvh" aria-labelledby="hero-title">
    <picture class="flex h-full w-full overflow-hidden z-0">
      <img
        src="/hero_img.jpg"
        alt="heroimage"
        class="w-full h-full object-cover object-center"
      />
    </picture>
    <u-container class="absolute z-10 left-0 right-0 top-0 bottom-0 py-24">
      <div class="flex flex-col gap-6 items-start h-full justify-between">
        <div
          class="flex max-xl:gap-6 justify-end max-xl:flex-col w-full h-full xl:items-end xl:justify-between"
        >
          <div class="flex max-w-3xl flex-col justify-end gap-2">
            <AppLogo :label="'Учебный портал'" class="w-fit" size="2xl" />

            <u-card class="w-fit">
              <p class="text-2xl font-semibold text-pretty text-shadow-lg">
                Современная платформа для обучения и взаимодействия студентов и
                преподавателей
              </p>
            </u-card>
            <div class="flex mt-2 max-md:flex-wrap gap-4 w-full">
              <u-card v-for="stat in stats" :key="stat.label" class="h-fit flex-2/5">
                <div class="flex flex-col justify-between gap-2">
                  <p class="text-3xl text-secondary font-semibold">{{ stat.value }}</p>
                  <p class="text-base truncate">{{ stat.label }}</p>
                </div>
              </u-card>
            </div>
          </div>
          <u-card class="w-fit">
            <div class="flex flex-wrap items-center gap-2.5">
              <u-button
                v-for="link in heroLinks"
                :key="link.label"
                :to="link.to"
                :color="link.color"
                :variant="link.variant"
                :size="link.size"
                :class="link.class"
                :trailing-icon="link.trailingIcon ? link.trailingIcon : undefined"
                class="max-md:w-full justify-center max-md:py-2.5"
              >
                {{ link.label }}
              </u-button>
            </div></u-card
          >
        </div>
      </div>
    </u-container>
  </section>
</template>
