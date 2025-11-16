<script setup lang="ts">
// Анимационное состояние
const isVisible = ref(false);

// Статистика для отображения
const stats = [
  { label: "Студентов", value: "10,000+", icon: "i-heroicons-users" },
  { label: "Курсов", value: "500+", icon: "i-heroicons-book-open" },
  { label: "Преподавателей", value: "200+", icon: "i-heroicons-academic-cap" },
];

// Инициализация анимации
onMounted(() => {
  nextTick(() => {
    isVisible.value = true;
  });
});

// Обработчик клика на кнопку
const handleRegister = () => {
  navigateTo("/auth/register");
};
</script>

<template>
  <section class="py-16 lg:py-24">
    <div class="container mx-auto">
      <!-- Статистика -->
      <div
        class="grid grid-cols-3 gap-8 mb-16"
        :class="[
          'transition-all duration-700 ease-out',
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8',
        ]"
      >
        <div
          v-for="(stat, index) in stats"
          :key="stat.label"
          class="text-center"
          :class="[
            'transition-all duration-500 ease-out',
            { 'delay-200': index === 1, 'delay-400': index === 2 },
          ]"
        >
          <div class="text-2xl lg:text-3xl font-bold text-highlighted mb-1">
            {{ stat.value }}
          </div>
          <div class="text-sm text-muted font-medium">
            {{ stat.label }}
          </div>
        </div>
      </div>

      <!-- Основной CTA -->
      <UCard
        :class="[
          'transition-all duration-700 ease-out delay-600',
          isVisible
            ? 'opacity-100 translate-y-0 scale-100'
            : 'opacity-0 translate-y-8 scale-95',
        ]"
      >
        <div class="text-center py-12 lg:py-16">
          <h2 class="text-3xl lg:text-4xl font-bold mb-4 text-highlighted">
            Готовы начать свое обучение?
          </h2>

          <p class="text-lg text-muted mb-8 max-w-2xl mx-auto leading-relaxed">
            Присоединяйтесь к тысячам студентов, которые уже улучшают свои
            навыки с нашей платформой.
          </p>

          <div
            class="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <UButton
              color="primary"
              size="xl"
              label="Начать бесплатно"
              trailing-icon="i-heroicons-arrow-right"
              @click="handleRegister"
            />

            <UButton
              to="/courses"
              color="neutral"
              variant="outline"
              size="xl"
              label="Посмотреть курсы"
            />
          </div>

          <div class="mt-8 pt-8 border-t border-border">
            <div
              class="flex flex-wrap justify-center items-center gap-6 text-sm text-muted"
            >
              <div class="flex items-center gap-2">
                <UIcon
                  name="i-heroicons-check-circle"
                  class="size-4 text-green-500"
                />
                <span>Бесплатный доступ</span>
              </div>
              <div class="flex items-center gap-2">
                <UIcon
                  name="i-heroicons-check-circle"
                  class="size-4 text-green-500"
                />
                <span>Не требует кредитной карты</span>
              </div>
              <div class="flex items-center gap-2">
                <UIcon
                  name="i-heroicons-check-circle"
                  class="size-4 text-green-500"
                />
                <span>Отмена в любое время</span>
              </div>
            </div>
          </div>
        </div>
      </UCard>

      <!-- Социальное доказательство -->
      <div
        class="mt-12 text-center"
        :class="[
          'transition-all duration-700 ease-out delay-800',
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8',
        ]"
      >
        <p class="text-sm text-muted mb-4">
          Доверяют ведущие компании и учебные заведения
        </p>
        <div
          class="flex flex-wrap justify-center items-center gap-8 opacity-60"
        >
          <!-- Плейсхолдеры для логотипов компаний -->
          <div class="flex items-center gap-2 text-muted">
            <UIcon name="i-heroicons-building-office" class="size-6" />
            <span class="font-semibold">TechCorp</span>
          </div>
          <div class="flex items-center gap-2 text-muted">
            <UIcon name="i-heroicons-academic-cap" class="size-6" />
            <span class="font-semibold">Университет</span>
          </div>
          <div class="flex items-center gap-2 text-muted">
            <UIcon name="i-heroicons-cpu-chip" class="size-6" />
            <span class="font-semibold">DevAcademy</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
