<script setup lang="ts">
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
const heroLinks = computed(() =>
  !isAuthenticated
    ? [
        {
          label: "Начать обучение",
          to: "/auth/register",
          color: "primary" as const,
          size: "xl" as const,
          trailingIcon: "i-heroicons-arrow-right",
          class: "group/btn",
        },
        {
          label: "Посмотреть курсы",
          to: "/courses",
          color: "neutral" as const,
          variant: "subtle" as const,
          size: "xl" as const,
          class: "group/btn",
        },
      ]
    : [
        {
          label: "Мои курсы",
          to: "/dashboard/courses",
          color: "primary" as const,
          size: "xl" as const,
          trailingIcon: "i-heroicons-arrow-right",
          class: "group/btn",
        },
      ]
);

// Анимационные состояния
const imageLoaded = ref(false);

// Обработчик загрузки изображения
const onImageLoad = () => {
  imageLoaded.value = true;
};
</script>

<template>
  <section class="relative py-16 lg:py-24" aria-labelledby="hero-title">
    <UPageHero
      title="Добро пожаловать в Учебный портал"
      description="Современная платформа для эффективного обучения и взаимодействия между студентами и преподавателями"
      orientation="horizontal"
      reverse
      :links="heroLinks"
      class="relative z-10"
    >
      <!-- Контейнер изображения с анимацией -->
      <div class="relative">
        <!-- Основное изображение -->
        <NuxtImg
          src="/hello-pic.png"
          alt="Учебный портал - современная платформа для обучения"
          class="rounded-lg shadow-lg"
          :class="[
            'transition-all duration-500',
            imageLoaded ? 'opacity-100 scale-100' : 'opacity-0 scale-95',
          ]"
          width="600"
          height="600"
          loading="eager"
          @load="onImageLoad"
        />
      </div>
    </UPageHero>
  </section>
</template>
