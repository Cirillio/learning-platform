<script setup lang="ts">
const { getCategories } = useCourses();

const {
  data: categoriesResponse,
  pending: categoriesPending,
  error: categoriesError,
} = await getCategories({
  page: 1,
  page_size: 4,
  ordering: "-created_at",
});

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
    description:
      "Отслеживание прогресса обучения, оценок и достижений в личном кабинете",
    color: "text-primary",
  },
];
</script>

<template>
  <section
    class="pt-12 pb-10 bg-default shadow-sm"
    aria-labelledby="features-title"
  >
    <layout-container class="w-full">
      <div
        class="flex max-md:flex-col max-md:text-center max-md:gap-2 items-center justify-between gap-2"
      >
        <div class="max-md:space-y-2">
          <h2 class="text-3xl font-bold">Выберите то, что вам интересно</h2>
          <p class="text-muted">
            Изучайте курсы по различным категориям и развивайте свои навыки
          </p>
        </div>
        <u-button
          trailing-icon="heroicons:arrow-right"
          label="Все категории"
          size="lg"
          variant="subtle"
          color="neutral"
          class="shadow-xs"
        />
      </div>
    </layout-container>
    <u-separator class="my-2" />

    <layout-container
      class="flex overflow-y-scroll hide-scrollbar pb-2 pt-10 gap-4"
    >
      <u-card
        v-for="category in categoriesResponse?.results"
        :key="category.slug"
        :ui="{
          header: '!p-0',
          root: 'max-w-lg w-full flex-shrink-0 shadow-sm bg-muted/75 dark:bg-muted/25 hover:bg-muted/50 dark:hover:bg-muted/35 transition-colors duration-200 ease-in-out',
        }"
      >
        <template #header>
          <div class="aspect-video overflow-hidden relative">
            <nuxt-img
              :src="category.icon"
              class="object-cover object-top z-0 w-full h-full transition-transform duration-300 ease-in-out"
            />

            <div
              class="absolute bottom-0 left-0 right-0 h-24 bg-linear-to-t from-default/30 dark:from-default/75 to-default/0"
            ></div>
            <div
              class="absolute z-30 rounded-sm px-2 py-1 top-2 left-2 border border-primary font-semibold bg-default/90 backdrop-blur-sm text-sm"
            >
              Новое
            </div>
          </div>
        </template>

        <nuxt-link
          :to="'/courses/categories/' + category.slug"
          class="flex items-center justify-between w-full text-default hover:text-primary transition-colors duration-200 group/title"
        >
          <h3 class="text-3xl font-bold">{{ category.name }}</h3>

          <UIcon
            name="heroicons:arrow-right"
            class="size-6 opacity-25 group-hover/title:opacity-100 transition-opacity duration-200"
          />
        </nuxt-link>
        <p class="text-muted line-clamp-2 truncate">
          {{ category.description }}
        </p>
      </u-card>
    </layout-container>
  </section>
</template>
