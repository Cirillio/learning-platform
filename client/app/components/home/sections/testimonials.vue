<script setup lang="ts">
// Отзывы студентов
const testimonials = [
  {
    name: "Анна Петрова",
    role: "Frontend разработчик",
    avatar:
      "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
    content:
      "Отличная платформа! Курсы очень качественные, преподаватели - профессионалы. За 6 месяцев прошел 3 курса и нашел работу мечты.",
    rating: 5,
    course: "React & Vue.js",
    delay: 0,
  },
  {
    name: "Михаил Иванов",
    role: "Data Scientist",
    avatar:
      "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
    content:
      "Практические задания на уровне реальных проектов. Получил не только знания, но и портфолио для трудоустройства.",
    rating: 5,
    course: "Python для Data Science",
    delay: 200,
  },
  {
    name: "Елена Смирнова",
    role: "UX Designer",
    avatar:
      "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
    content:
      "Курсы по дизайну превзошли все ожидания. Преподаватели делятся реальным опытом из индустрии.",
    rating: 5,
    course: "UX/UI Design",
    delay: 400,
  },
];

// Анимационное состояние
const isVisible = ref(false);

// Инициализация анимации
onMounted(() => {
  nextTick(() => {
    isVisible.value = true;
  });
});
</script>

<template>
  <section class="py-16 lg:py-24">
    <div class="container mx-auto px-4">
      <!-- Заголовок секции -->
      <div class="text-center mb-16">
        <h2
          class="text-3xl lg:text-4xl font-bold mb-4 text-highlighted"
          :class="[
            'transition-all duration-700 ease-out',
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8',
          ]"
        >
          Что говорят наши студенты
        </h2>
        <p
          class="text-lg text-muted max-w-2xl mx-auto"
          :class="[
            'transition-all duration-700 ease-out delay-200',
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8',
          ]"
        >
          Реальные отзывы от студентов, которые уже прошли обучение на нашей
          платформе
        </p>
      </div>

      <!-- Сетка отзывов -->
      <div class="grid lg:grid-cols-3 gap-8">
        <UCard
          v-for="(testimonial, index) in testimonials"
          :key="testimonial.name"
          class="h-full"
          :class="[
            'transition-all duration-700 ease-out',
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8',
          ]"
          :style="{ transitionDelay: `${testimonial.delay}ms` }"
        >
          <!-- Рейтинг -->
          <div class="flex items-center gap-1 mb-4">
            <UIcon
              v-for="star in testimonial.rating"
              :key="star"
              name="i-heroicons-star"
              class="size-5 text-yellow-400 fill-current"
            />
          </div>

          <!-- Отзыв -->
          <blockquote class="text-muted mb-6 leading-relaxed italic">
            "{{ testimonial.content }}"
          </blockquote>

          <!-- Автор -->
          <div class="flex items-center gap-4">
            <UAvatar
              :src="testimonial.avatar"
              :alt="testimonial.name"
              size="lg"
            />

            <div>
              <div class="font-semibold text-highlighted">
                {{ testimonial.name }}
              </div>
              <div class="text-sm text-muted">
                {{ testimonial.role }}
              </div>
              <div class="text-xs text-primary font-medium mt-1">
                Курс: {{ testimonial.course }}
              </div>
            </div>
          </div>
        </UCard>
      </div>

      <!-- CTA для отзывов -->
      <div
        class="mt-16 text-center"
        :class="[
          'transition-all duration-700 ease-out delay-600',
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8',
        ]"
      >
        <div class="inline-flex items-center gap-2 px-6 py-3">
          <UIcon
            name="i-heroicons-chat-bubble-left-right"
            class="size-5 text-primary"
          />
          <span class="text-sm font-medium text-primary">
            Более 2,000 положительных отзывов на платформе
          </span>
        </div>
      </div>
    </div>
  </section>
</template>
