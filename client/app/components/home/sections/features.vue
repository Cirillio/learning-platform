<script setup lang="ts">
// Данные для фич
const features = [
  {
    icon: "i-heroicons-book-open",
    title: "Курсы",
    description:
      "Широкий выбор курсов от опытных преподавателей по различным направлениям",
    color: "text-primary",
  },
  {
    icon: "i-heroicons-clipboard-document-check",
    title: "Задания",
    description:
      "Практические задания с возможностью загрузки файлов и получения обратной связи",
    color: "text-primary",
  },
  {
    icon: "i-heroicons-chart-bar",
    title: "Прогресс",
    description: "Отслеживание прогресса обучения, оценок и достижений в личном кабинете",
    color: "text-primary",
  },
];
</script>

<template>
  <section class="py-16 lg:py-24" aria-labelledby="features-title">
    <div class="container mx-auto">
      <!-- Заголовок секции -->
      <div class="text-center mb-16">
        <h2
          id="features-title"
          class="text-3xl lg:text-4xl font-bold mb-4 text-highlighted"
        >
          Почему выбирают нас
        </h2>
        <p class="text-lg text-muted max-w-2xl mx-auto">
          Наша платформа предоставляет все необходимое для эффективного обучения
        </p>
      </div>

      <!-- Сетка фич -->
      <div class="grid md:grid-cols-3 gap-8">
        <UCard v-for="(feature, index) in features" :key="feature.title" class="h-full">
          <template #header>
            <div class="flex items-center gap-3">
              <UIcon :name="feature.icon" class="size-8 text-primary" />
              <h3 class="text-xl font-semibold">
                {{ feature.title }}
              </h3>
            </div>
          </template>

          <p class="text-muted leading-relaxed">
            {{ feature.description }}
          </p>
        </UCard>
      </div>

      <!-- Дополнительная информация -->
      <div class="mt-16 text-center">
        <div class="inline-flex items-center gap-2 px-4 py-2 text-sm text-muted">
          <UIcon name="i-heroicons-check-circle" class="size-4 text-green-500" />
          <span>Более 10,000 студентов уже выбрали нашу платформу</span>
        </div>
      </div>
    </div>
  </section>
</template>
