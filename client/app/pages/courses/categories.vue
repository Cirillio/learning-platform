<script lang="ts" setup>
definePageMeta({
  layout: "courses-catalog",
});

const { getCategories } = useCourses();
const { data: categoriesResponse, pending, error } = await getCategories();

const unwatchCategories = watch(
  () => categoriesResponse,
  (newVal) => {
    console.log("Fetched categories:", newVal);
  }
);

// Очистка watch при размонтировании страницы
onUnmounted(() => {
  unwatchCategories();
});
</script>

<template>
  {{ error }}
  <UContainer>
    <UPageHeader
      title="Категории курсов"
      description="Выберите направление, которое вам интересно, и начните обучение."
    />

    <CoursesCategoryList
      :categories="categoriesResponse?.results"
      :loading="pending"
      :error="error ?? null"
    />
  </UContainer>
</template>
