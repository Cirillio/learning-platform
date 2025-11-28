<script lang="ts" setup>
const { isAuthenticated, user } = useAuthStore();
const { logout } = useAuth();
</script>

<template>
  <UPopover
    :ui="{
      content:
        'max-w-48 w-dvw translate-y-2 shadow-xl py-3 px-2 md:hidden bg-default/92 backdrop-blur-xs',
    }"
  >
    <slot />

    <template #content>
      <div class="flex w-full flex-col gap-2 md:hidden">
        <USeparator color="neutral" />

        <h3 class="text-sm px-2 font-semibold text-muted tracking-wider">
          Аккаунт
        </h3>

        <div v-if="isAuthenticated" class="flex flex-col gap-2">
          <div class="flex justify-between">
            <span class="font-normal text-lg px-2">{{
              user?.role == "student" ? "Студент" : "Преподаватель"
            }}</span>
          </div>
          <USeparator />
          <HeaderMobileUserActions :user="user" />
        </div>

        <HeaderMobileAuth v-else />

        <USeparator color="neutral" />

        <h3 class="text-sm px-2 font-semibold text-muted tracking-wider">
          Навигация
        </h3>

        <HeaderMobileNavigation />
        <USeparator color="neutral" />

        <HeaderMobileActions v-if="isAuthenticated" v-on:logout="logout" />
        <USeparator v-if="isAuthenticated" color="neutral" />
      </div>
    </template>
  </UPopover>
</template>
