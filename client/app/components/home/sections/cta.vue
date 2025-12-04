<script setup lang="ts">
// Обработчик клика на кнопку
const handleRegister = () => {
  navigateTo("/auth/register");
};

const trustedByCompanies = [
  "heroicons:cpu-chip",
  "heroicons:academic-cap",
  "heroicons:building-library",
  "heroicons:globe-alt",
  "heroicons:light-bulb",
  "heroicons:briefcase",
  "heroicons:circle-stack",
];
</script>

<template>
  <section
    class="py-16 lg:py-24 bg-default shadow-sm"
    aria-labelledby="cta-title"
  >
    <LayoutContainer>
      <!-- Основной CTA -->
      <UCard
        :ui="{
          root: 'dark:bg-muted/25 bg-muted/75 group',
          body: 'flex max-md:flex-col gap-2 !py-2 md:!py-0 !px-2',
        }"
      >
        <div class="flex-1/2 min-w-0 h-fit my-auto py-8 px-4">
          <h2 class="text-3xl font-bold">Готовы начать свое обучение?</h2>

          <p class="text-muted">
            Присоединяйтесь к тысячам студентов, которые уже улучшают свои
            навыки с нашей платформой.
          </p>

          <div class="flex flex-col mt-6 lg:flex-row gap-2">
            <UButton
              color="primary"
              size="xl"
              label="Начать бесплатно"
              trailing-icon="i-heroicons-arrow-right"
              @click="handleRegister"
              class="w-fit"
            />

            <UButton
              to="/courses"
              color="neutral"
              variant="outline"
              size="xl"
              label="Посмотреть курсы"
              class="w-fit"
            />
          </div>

          <USeparator class="my-4" />

          <div class="w-fit">
            <div class="flex flex-wrap gap-2 text-sm text-muted">
              <div class="flex items-center gap-1">
                <UIcon
                  name="i-heroicons-check-circle"
                  class="size-4 text-green-500"
                />
                <span>Бесплатный доступ</span>
              </div>
              <div class="flex items-center gap-1">
                <UIcon
                  name="i-heroicons-check-circle"
                  class="size-4 text-green-500"
                />
                <span>Не требует кредитной карты</span>
              </div>
              <div class="flex items-center gap-1">
                <UIcon
                  name="i-heroicons-check-circle"
                  class="size-4 text-green-500"
                />
                <span>Отмена в любое время</span>
              </div>
            </div>
          </div>
        </div>

        <NuxtImg
          class="flex-1/2 min-w-0 object-cover rounded-xl lg:translate-y-16 shadow-xl border border-muted lg:scale-90 group-active:md:scale-100 group-active:md:translate-y-2 group-hover:md:scale-100 group-hover:md:translate-y-2 transition-transform duration-200 ease-out"
          src="/home_page_cta.png"
        />
      </UCard>

      <!-- Социальное доказательство -->
      <UPageLogos
        class="mt-12 max-w-4xl mx-auto"
        title="Доверяют ведущие компании и учебные заведения"
        marquee
        :items="trustedByCompanies"
      />
    </LayoutContainer>
  </section>
</template>
