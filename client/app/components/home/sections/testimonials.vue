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
  },
];
</script>

<template>
  <section
    class="pt-12 pb-10 bg-default shadow-sm"
    aria-labelledby="testimonials-title"
  >
    <LayoutContainer class="w-full">
      <!-- Заголовок секции -->
      <h2 class="text-3xl font-bold">Что говорят наши студенты</h2>
      <p class="text-muted">
        Реальные отзывы от студентов, которые уже прошли обучение на нашей
        платформе
      </p>
    </LayoutContainer>
    <USeparator class="my-2" />
    <LayoutContainer class="w-full pb-2 pt-10">
      <!-- Сетка отзывов -->
      <div class="grid lg:grid-cols-3 gap-4">
        <UCard
          v-for="(testimonial, index) in testimonials"
          :key="testimonial.name"
          class="h-full"
          :ui="{
            body: '!p-4 flex flex-col gap-3',
            root: 'bg-muted/75 dark:bg-muted/25 hover:bg-muted/25 dark:hover:bg-muted/35 transition-all duration-200 ease-in-out shadow-sm',
          }"
        >
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
            </div>
          </div>
          <!-- Рейтинг -->
          <div class="flex items-center gap-1">
            <UIcon
              v-for="star in testimonial.rating"
              :key="star"
              name="i-heroicons-star-solid"
              class="size-5 text-yellow-400 fill-current"
            />
          </div>

          <div class="text-sm text-primary font-semibold">
            Курс: {{ testimonial.course }}
          </div>

          <!-- Отзыв -->
          <blockquote class="text-default/90 leading-relaxed">
            "{{ testimonial.content }}"
          </blockquote>
        </UCard>
      </div>

      <!-- CTA для отзывов -->
      <div class="mt-4 text-center">
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
    </LayoutContainer>
  </section>
</template>
