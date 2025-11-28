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

const { isAuthenticated, login } = useAuth();

const onStart = () => {
  if (!isAuthenticated) {
    navigateTo("/auth/login");
  } else {
    // Перенаправление на страницу курсов пользователя
    navigateTo("/courses");
  }
};

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
  <section
    class="relative shadow-md flex border-b border-muted"
    aria-labelledby="hero-title"
  >
    <NuxtImg
      :src="'/home_page_hero.png'"
      @load="onImageLoad"
      class="object-cover object-center w-full h-[448px] md:h-[648px] lg:h-[868px]"
    />
    <div
      class="absolute top-3/5 md:top-4/5 left-0 right-0 bottom-0 z-10 bg-linear-to-t from-black to-black/0"
    ></div>
    <LayoutContainer
      class="absolute z-20 left-0 right-0 top-0 bottom-0 py-8 md:py-16"
    >
      <div class="flex flex-col gap-6 items-start size-full justify-between">
        <div class="flex max-xl:gap-2 flex-col justify-end h-full w-full">
          <AppLogo
            class="size-12 lg:size-16 lg:self-end md:mb-auto animate-pulse text-primary!"
          />
          <div
            class="flex w-full max-lg:flex-col max-lg:items-start max-lg:gap-6 gap-2 justify-between items-end"
          >
            <div
              class="flex max-w-5xl flex-col text-white justify-between h-full gap-1 md:gap-2"
            >
              <h1
                id="hero-title"
                class="text-3xl md:text-5xl lg:text-7xl text-balance max-md:font-bold font-medium text-shadow-md"
              >
                Образовательный портал
              </h1>
              <h2
                class="text-base md:text-xl max-md:font-normal font-extralight text-pretty text-shadow-md"
              >
                Современная платформа для обучения и взаимодействия студентов и
                преподавателей
              </h2>
            </div>

            <UButton
              label="Начать"
              trailing-icon="heroicons:arrow-right-20-solid"
              class="text-base lg:text-xl shadow-md"
              color="primary"
              @click="onStart"
            />
          </div>
        </div>
      </div>
    </LayoutContainer>
  </section>
</template>
