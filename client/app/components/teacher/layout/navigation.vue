<script lang="ts" setup>
import type { NavigationMenuItem } from "@nuxt/ui";

const cookie = useCookie<boolean>("teacher-sidebar-collapsed", {
  default: () => false,
});

const isSidebarCollapsed = useState<boolean>(
  "teacher-sidebar-collapsed",
  () => false
);

onMounted(() => {
  isSidebarCollapsed.value = cookie.value;
});

watch(isSidebarCollapsed, (val) => {
  cookie.value = val;
});

// Navigation items
const navItems = ref<NavigationMenuItem[]>([
  {
    label: "Панель управления",
    icon: "i-lucide-layout-dashboard",
    to: "/teacher/dashboard",
  },
  {
    label: "Мои курсы",
    icon: "i-lucide-book-open",
    to: "/teacher/courses",
  },
  {
    label: "Проверка работ",
    icon: "i-lucide-clipboard-check",
    to: "/teacher/grading",
  },
  {
    label: "Студенты",
    icon: "i-lucide-users",
    to: "/teacher/students",
  },
]);
</script>

<template>
  <UNavigationMenu
    :collapsed="isSidebarCollapsed"
    :items="navItems"
    orientation="vertical"
    :ui="{
      root: isSidebarCollapsed ? 'w-fit' : '',
      list: 'space-y-1',
      link: `text-lg`,
      linkLeadingIcon: 'size-6',
    }"
  >
  </UNavigationMenu>
</template>
