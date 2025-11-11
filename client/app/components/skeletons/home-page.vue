<script setup lang="ts">
// Анимационные состояния для имитации загрузки
const isVisible = ref(false);

onMounted(() => {
  nextTick(() => {
    isVisible.value = true;
  });
});
</script>

<template>
  <div class="animate-pulse">
    <!-- Hero Section Skeleton -->
    <section class="relative py-16 lg:py-24">
      <div class="container mx-auto px-4">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <!-- Левая колонка - текст -->
          <div class="space-y-6">
            <!-- Заголовок -->
            <div class="space-y-3">
              <USkeleton class="h-12 w-3/4" />
              <USkeleton class="h-12 w-1/2" />
            </div>

            <!-- Описание -->
            <div class="space-y-2">
              <USkeleton class="h-4 w-full" />
              <USkeleton class="h-4 w-5/6" />
              <USkeleton class="h-4 w-4/6" />
            </div>

            <!-- Кнопки -->
            <div class="flex flex-col sm:flex-row gap-4 pt-4">
              <USkeleton class="h-12 w-40" />
              <USkeleton class="h-12 w-40" />
            </div>
          </div>

          <!-- Правая колонка - изображение -->
          <div class="flex justify-center lg:justify-end">
            <USkeleton class="w-full max-w-md h-96 rounded-lg" />
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section Skeleton -->
    <section class="py-16 lg:py-24">
      <div class="container mx-auto px-4">
        <!-- Заголовок секции -->
        <div class="text-center mb-16 space-y-4">
          <USkeleton class="h-10 w-80 mx-auto" />
          <USkeleton class="h-6 w-96 mx-auto" />
        </div>

        <!-- Сетка фич -->
        <div class="grid md:grid-cols-3 gap-8">
          <UCard
            v-for="n in 3"
            :key="n"
            class="h-64"
            :class="[
              'transition-all duration-700 ease-out',
              isVisible
                ? 'opacity-100 translate-y-0'
                : 'opacity-0 translate-y-8',
            ]"
            :style="{ transitionDelay: `${(n - 1) * 200}ms` }"
          >
            <template #header>
              <div class="flex items-center gap-3">
                <USkeleton class="size-8 rounded" />
                <USkeleton class="h-6 w-24" />
              </div>
            </template>

            <div class="space-y-2">
              <USkeleton class="h-4 w-full" />
              <USkeleton class="h-4 w-5/6" />
              <USkeleton class="h-4 w-4/6" />
            </div>
          </UCard>
        </div>

        <!-- Дополнительная информация -->
        <div class="mt-16 flex justify-center">
          <USkeleton class="h-8 w-80 rounded-full" />
        </div>
      </div>
    </section>

    <!-- Testimonials Section Skeleton -->
    <section class="py-16 lg:py-24">
      <div class="container mx-auto px-4">
        <!-- Заголовок секции -->
        <div class="text-center mb-16 space-y-4">
          <USkeleton class="h-10 w-80 mx-auto" />
          <USkeleton class="h-6 w-96 mx-auto" />
        </div>

        <!-- Сетка отзывов -->
        <div class="grid lg:grid-cols-3 gap-8">
          <UCard
            v-for="n in 3"
            :key="n"
            class="h-80"
            :class="[
              'transition-all duration-700 ease-out',
              isVisible
                ? 'opacity-100 translate-y-0'
                : 'opacity-0 translate-y-8',
            ]"
            :style="{ transitionDelay: `${(n - 1) * 200}ms` }"
          >
            <!-- Рейтинг -->
            <div class="flex gap-1 mb-4">
              <USkeleton v-for="star in 5" :key="star" class="size-5 rounded" />
            </div>

            <!-- Отзыв -->
            <div class="space-y-2 mb-6">
              <USkeleton class="h-4 w-full" />
              <USkeleton class="h-4 w-5/6" />
              <USkeleton class="h-4 w-4/6" />
            </div>

            <!-- Автор -->
            <div class="flex items-center gap-4">
              <USkeleton class="size-12 rounded-full" />
              <div class="space-y-2">
                <USkeleton class="h-4 w-32" />
                <USkeleton class="h-3 w-24" />
                <USkeleton class="h-3 w-28" />
              </div>
            </div>
          </UCard>
        </div>

        <!-- CTA для отзывов -->
        <div class="mt-16 flex justify-center">
          <USkeleton class="h-8 w-64 rounded-full" />
        </div>
      </div>
    </section>

    <!-- CTA Section Skeleton -->
    <section class="py-16 lg:py-24">
      <div class="container mx-auto px-4">
        <!-- Статистика -->
        <div class="grid grid-cols-3 gap-8 mb-16">
          <div
            v-for="n in 3"
            :key="n"
            class="text-center space-y-2"
            :class="[
              'transition-all duration-500 ease-out',
              isVisible
                ? 'opacity-100 translate-y-0'
                : 'opacity-0 translate-y-8',
            ]"
            :style="{ transitionDelay: `${(n - 1) * 200}ms` }"
          >
            <USkeleton class="h-8 w-20 mx-auto" />
            <USkeleton class="h-4 w-16 mx-auto" />
          </div>
        </div>

        <!-- Основной CTA -->
        <UCard class="mb-12">
          <div class="text-center py-12 lg:py-16 space-y-6">
            <USkeleton class="h-10 w-80 mx-auto" />
            <div class="space-y-2">
              <USkeleton class="h-6 w-full max-w-2xl mx-auto" />
              <USkeleton class="h-6 w-5/6 max-w-2xl mx-auto" />
            </div>

            <div class="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <USkeleton class="h-12 w-40" />
              <USkeleton class="h-12 w-40" />
            </div>

            <div class="mt-8 pt-8 border-t border-border">
              <div class="flex flex-wrap justify-center gap-6">
                <div v-for="n in 3" :key="n" class="flex items-center gap-2">
                  <USkeleton class="size-4 rounded-full" />
                  <USkeleton class="h-4 w-32" />
                </div>
              </div>
            </div>
          </div>
        </UCard>

        <!-- Социальное доказательство -->
        <div class="text-center space-y-4">
          <USkeleton class="h-4 w-64 mx-auto" />
          <div class="flex justify-center gap-8">
            <div v-for="n in 3" :key="n" class="flex items-center gap-2">
              <USkeleton class="size-6 rounded" />
              <USkeleton class="h-4 w-24" />
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
