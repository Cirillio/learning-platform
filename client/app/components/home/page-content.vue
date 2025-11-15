<script setup lang="ts">
// SEO мета-теги для главной страницы
useSeoMeta({
  title: "Главная - Учебный портал",
  description:
    "Современная платформа для обучения и взаимодействия студентов и преподавателей",
});
</script>

<template>
  <div>
    <!-- Hero Section -->
    <HomeSectionsHero />

    <!-- Features Section -->
    <HomeSectionsFeatures />

    <!-- Testimonials Section -->
    <HomeSectionsTestimonials />

    <!-- CTA Section -->
    <HomeSectionsCta />
  </div>
</template>
