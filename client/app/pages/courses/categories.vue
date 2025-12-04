<script lang="ts" setup>
const { getCategories } = useCourses();
const {
  data: categoriesResponse,
  pending,
  error,
} = await getCategories({
  page_size: 100,
});
</script>

<template>
  <div class="space-y-2 bg-default border-b border-muted">
    <CoursesHero
      title="Категории курсов"
      description="Выберите направление, которое вам интересно, и начните обучение."
      class="shadow-sm"
    />

    <LayoutContainer class="py-8 bg-muted/25 mb-2 shadow-sm">
      <CoursesCatalogCategoryGrid
        :categories="categoriesResponse?.results"
        :loading="pending"
        :error="error ?? null"
      />
    </LayoutContainer>
  </div>
</template>
