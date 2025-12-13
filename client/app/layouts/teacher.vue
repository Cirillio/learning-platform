<script setup lang="ts">
import type { NavigationMenuItem } from "@nuxt/ui";

const route = useRoute();
const authStore = useAuthStore();

const isSidebarCollapsed = useState<boolean>(
  "teacher-sidebar-collapsed",
  () => false
);

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};
</script>

<template>
  <div class="p-2 grid min-h-dvh">
    <UCard
      :ui="{
        root: ' h-full',
        body: 'flex  bg-default h-full !p-0',
      }"
    >
      <!-- Sidebar -->
      <aside
        class="border-r h-full min-h-0 border-default transition-all duration-300 z-40 flex flex-col"
      >
        <!-- Logo -->
        <div
          class="h-16 flex items-center justify-between px-3 border-b border-default shrink-0"
        >
          <div
            v-if="!isSidebarCollapsed"
            class="flex items-center p-2 w-full gap-2"
          >
            <div
              class="size-10 rounded-lg bg-primary flex items-center justify-center"
            >
              <UIcon
                name="i-lucide-graduation-cap"
                class="size-8 text-inverted"
              />
            </div>
            <div class="flex flex-col leading-5 text-xl">
              <span class="font-bold text-default">Панель</span>
              <span class="font-bold text-default">Учителя</span>
            </div>
          </div>
          <div
            v-else
            class="size-8 rounded-lg bg-primary flex items-center justify-center mx-auto"
          >
            <UIcon
              name="i-lucide-graduation-cap"
              class="size-5 text-inverted"
            />
          </div>
        </div>

        <!-- Navigation -->
        <div class="overflow-y-auto flex p-3 boder">
          <TeacherLayoutNavigation />
        </div>

        <USeparator />

        <!-- User Section -->
        <div class="p-3">
          <UButton
            to="/teacher"
            :icon="isSidebarCollapsed ? 'heroicons:user' : undefined"
            variant="outline"
            color="neutral"
            class="justify-start"
            :ui="{
              base: isSidebarCollapsed ? 'w-fit px-1.5' : 'w-full',
              leadingIcon: 'size-6',
            }"
          >
            <div class="flex flex-col items-start" v-if="!isSidebarCollapsed">
              <span class="text-xl font-medium text-default truncate">
                {{ authStore.user?.first_name }} {{ authStore.user?.last_name }}
              </span>
              <span class="text-sm text-muted">Преподаватель</span>
            </div>
          </UButton>
        </div>

        <USeparator />

        <div class="p-3">
          <UButton
            :icon="
              isSidebarCollapsed
                ? 'i-lucide-chevron-right'
                : 'i-lucide-chevron-left'
            "
            :label="isSidebarCollapsed ? '' : 'Свернуть'"
            color="neutral"
            variant="soft"
            :class="
              isSidebarCollapsed ? 'justify-center px-2 ' : ' justify-start'
            "
            @click="toggleSidebar"
            block
            :ui="{
              leadingIcon: isSidebarCollapsed ? '-mr-2' : '',
            }"
          />
        </div>
      </aside>

      <!-- Main Content -->
      <div class="flex-1 flex flex-col transition-all duration-300">
        <!-- Header -->
        <header class="p-3 h-16 border-b border-default">
          <div class="h-full flex items-center justify-between">
            <div class="flex items-center gap-2">
              <UButton
                icon="heroicons:arrow-left"
                color="neutral"
                variant="ghost"
                size="lg"
                @click="$router.back"
              />
              <h1 class="text-2xl font-bold text-default">
                {{ route.meta.title || "Панель преподавателя" }}
              </h1>
            </div>

            <div class="flex items-center gap-4">
              <!-- Quick Actions -->
              <UButton
                to="/teacher/courses/create"
                icon="i-lucide-plus"
                color="primary"
                size="lg"
              >
                Новый курс
              </UButton>

              <!-- Notifications -->
              <UTooltip text="Уведомления">
                <UButton
                  icon="i-lucide-bell"
                  color="secondary"
                  variant="ghost"
                  size="lg"
              /></UTooltip>

              <UColorModeButton size="lg" color="success" />

              <!-- Back to main site -->
              <UTooltip text="Вернуться на сайт">
                <UButton
                  to="/"
                  icon="i-lucide-external-link"
                  color="info"
                  variant="ghost"
                  size="lg"
                />
              </UTooltip>

              <UButton
                to="/teacher/courses/create"
                icon="heroicons:arrow-right-on-rectangle"
                color="error"
                variant="ghost"
                size="lg"
              />
            </div>
          </div>
        </header>

        <!-- Content -->
        <main class="p-3">
          <slot />
        </main>
      </div>
    </UCard>
  </div>
</template>
