<template>
  <div class="flex min-h-screen">
    <!-- Collapsible Sidebar -->
    <LearningSidebar
      :is-collapsed="isSidebarCollapsed"
      @toggle="toggleSidebar"
    />

    <!-- Main Content Area -->
    <div
      class="flex-1 flex flex-col transition-all duration-300"
      :class="isSidebarCollapsed ? 'ml-16' : 'ml-72'"
    >
      <!-- Minimal Header -->
      <LearningHeader @toggle-sidebar="toggleSidebar" />

      <!-- Content -->
      <main class="flex-1 bg-default">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
const isSidebarCollapsed = useState("learning-sidebar-collapsed", () => false);

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};
</script>
