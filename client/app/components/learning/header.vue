<script setup lang="ts">
const emit = defineEmits<{
  toggleSidebar: [];
}>();

const route = useRoute();
const authStore = useAuthStore();

const courseSlug = computed(() => route.params.course_slug as string);
</script>

<template>
  <header
    class="sticky top-0 z-30 h-16 bg-elevated/80 backdrop-blur-md border-b border-default"
  >
    <div class="h-full px-6 flex items-center justify-between">
      <!-- Left: Toggle & Breadcrumbs -->
      <div class="flex items-center gap-4">
        <UButton
          icon="i-lucide-menu"
          color="neutral"
          variant="ghost"
          size="sm"
          @click="emit('toggleSidebar')"
        />

        <UBreadcrumb>
          <UBreadcrumbItem to="/learning" icon="i-lucide-home" />
          <UBreadcrumbItem :to="`/courses/${courseSlug}`" label="Курс" />
          <UBreadcrumbItem v-if="route.params.lesson_slug" label="Урок" />
        </UBreadcrumb>
      </div>

      <!-- Right: User Menu -->
      <div class="flex items-center gap-4">
        <!-- Exit Learning Mode -->
        <UTooltip text="Выйти из режима обучения">
          <UButton
            :to="`/courses/${courseSlug}`"
            icon="i-lucide-x"
            color="neutral"
            variant="ghost"
            size="sm"
          />
        </UTooltip>

        <!-- User Avatar -->
        <UDropdownMenu
          v-if="authStore.user"
          :items="[
            [
              { label: 'Профиль', icon: 'i-lucide-user', to: '/profile' },
              {
                label: 'Мои курсы',
                icon: 'i-lucide-book-open',
                to: '/learning',
              },
            ],
            [{ label: 'Выйти', icon: 'i-lucide-log-out', to: '/auth/logout' }],
          ]"
        >
          <UAvatar
            :alt="authStore.user.first_name || authStore.user.username"
            size="sm"
            class="cursor-pointer"
          />
        </UDropdownMenu>
      </div>
    </div>
  </header>
</template>
