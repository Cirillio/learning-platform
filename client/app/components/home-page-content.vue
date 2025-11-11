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
    <SectionsHero />

    <!-- Features Section -->
    <SectionsFeatures />

    <!-- Testimonials Section -->
    <SectionsTestimonials />

    <!-- CTA Section -->
    <SectionsCta />
  </div>
</template>
