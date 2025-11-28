<script lang="ts" setup></script>

<template>
  <div class="flex gap-1.5 items-center">
    <UButton
      to="/auth/login"
      variant="outline"
      color="secondary"
      icon="heroicons:user-circle"
      label="Войти"
    />
    <UButton
      to="/auth/register"
      color="primary"
      icon="heroicons:user-plus"
      label="Регистрация"
    />
  </div>
</template>
