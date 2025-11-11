<script setup lang="ts">
// SEO мета-теги теперь в компоненте Hero

// Состояние загрузки
const isLoading = ref(true);
const HomePageContent = ref();

// Асинхронная загрузка компонента
onMounted(async () => {
  try {
    // Динамический импорт компонента
    const component = await import("~/components/home-page-content.vue");
    HomePageContent.value = component.default;

    isLoading.value = false;
  } catch (error) {
    console.error("Ошибка загрузки компонента:", error);
    isLoading.value = false;
  }
});
</script>

<template>
  <!-- Показываем скелетон во время загрузки -->
  <SkeletonsHomePage v-if="isLoading" />

  <!-- Показываем контент после загрузки -->
  <component :is="HomePageContent" v-else />
</template>
