<script setup lang="ts">
// SEO мета-теги для Hero секции
useSeoMeta({
  title: "Главная - Учебный портал",
  description:
    "Современная платформа для обучения и взаимодействия студентов и преподавателей",
  ogImage: "/hello-pic.png",
  ogType: "website",
});

// Данные для кнопок
const heroLinks = [
  {
    label: "Начать обучение",
    to: "/auth/register",
    color: "secondary" as const,
    size: "xl" as const,
    trailingIcon: "i-heroicons-arrow-right",
    class: "group/btn",
  },
  {
    label: "Посмотреть курсы",
    to: "/courses",
    color: "neutral" as const,
    variant: "outline" as const,
    size: "xl" as const,
    class: "group/btn",
  },
];

// Анимационные состояния
const isVisible = ref(false);
const imageLoaded = ref(false);

// Обработчик загрузки изображения
const onImageLoad = () => {
  imageLoaded.value = true;
};

// Инициализация анимации при монтировании
onMounted(() => {
  nextTick(() => {
    isVisible.value = true;
  });
});
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
      :class="[
        'transition-all duration-1000 ease-out',
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8',
      ]"
    >
      <!-- Контейнер изображения с анимацией -->
      <div
        class="relative"
        :class="[
          'transition-all duration-700 ease-out delay-300',
          isVisible
            ? 'opacity-100 translate-x-0 scale-100'
            : 'opacity-0 translate-x-8 scale-95',
        ]"
      >
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

<style scoped>
/* Кастомные анимации */
@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.group\/image:hover .group\/image > :first-child {
  animation: float 3s ease-in-out infinite;
}
</style>
