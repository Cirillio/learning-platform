<template>
  <div>
    <h3 class="text-sm font-semibold text-muted uppercase tracking-wider mb-3">
      Аккаунт
    </h3>
    <div class="space-y-2">
      <UButton
        block
        to="/auth/login"
        variant="ghost"
        color="neutral"
        size="lg"
        icon="i-heroicons-arrow-right-end-on-rectangle"
        label="Войти"
        :ui="{
          leadingIcon: 'size-6',
          label: 'text-lg',
        }"
      />
      <UButton
        block
        to="/auth/register"
        color="secondary"
        size="lg"
        icon="i-heroicons-user-plus"
        label="Регистрация"
        :ui="{
          leadingIcon: 'size-6',
          label: 'text-lg',
        }"
      />
    </div>
  </div>
</template>
