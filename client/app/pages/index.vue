<script setup lang="ts">
// SEO мета-теги для главной страницы
useSeoMeta({
  title: "Главная - Учебный портал",
  description:
    "Современная платформа для обучения и взаимодействия студентов и преподавателей",
});
</script>

<template>
  <div class="space-y-2">
    <!-- Hero Section -->
    <HomeSectionsHero />

    <!-- Features Section -->
    <HomeSectionsFeaturedCategories />

    <!-- Testimonials Section -->
    <HomeSectionsTestimonials />

    <!-- CTA Section -->
    <HomeSectionsCta />
  </div>
</template>
