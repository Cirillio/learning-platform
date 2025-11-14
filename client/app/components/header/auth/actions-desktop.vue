<script lang="ts" setup></script>

<template>
  <div class="flex gap-1.5 items-center">
    <UButton
      to="/auth/login"
      variant="soft"
      color="secondary"
      size="lg"
      label="Войти"
      class="hidden sm:inline-flex"
    />

    <UButton size="lg" to="/auth/register" color="primary" label="Регистрация" />
  </div>
</template>
