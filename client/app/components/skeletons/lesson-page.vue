<script setup lang="ts">
// No props needed for skeleton
</script>

<template>
  <div class="min-h-screen bg-default">
    <!-- Header Skeleton -->
    <header class="bg-elevated border-b border-default">
      <UContainer class="py-6">
        <!-- Breadcrumbs Skeleton -->
        <div class="flex items-center gap-2 mb-4">
          <USkeleton class="h-4 w-16" />
          <USkeleton class="h-4 w-1" />
          <USkeleton class="h-4 w-20" />
          <USkeleton class="h-4 w-1" />
          <USkeleton class="h-4 w-24" />
        </div>

        <div
          class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4"
        >
          <!-- Title & Meta Skeleton -->
          <div class="space-y-2 flex-1">
            <div class="flex items-center gap-3">
              <USkeleton class="h-8 w-3/4" />
              <USkeleton class="h-6 w-20 rounded-full" />
            </div>

            <div class="flex items-center gap-4">
              <USkeleton class="h-4 w-16" />
              <USkeleton class="h-4 w-20" />
              <USkeleton class="h-4 w-24" />
            </div>
          </div>

          <!-- Progress Indicator Skeleton -->
          <div class="flex items-center gap-4">
            <div class="text-right space-y-1">
              <USkeleton class="h-4 w-24" />
              <USkeleton class="h-6 w-12" />
            </div>
            <USkeleton class="h-14 w-14 rounded-full" />
          </div>
        </div>
      </UContainer>
    </header>

    <!-- Main Content Skeleton -->
    <UContainer class="py-8">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <!-- Main Content Area Skeleton -->
        <div class="lg:col-span-8 space-y-8">
          <!-- Video Skeleton -->
          <div
            class="bg-elevated rounded-xl border border-default overflow-hidden"
          >
            <div class="p-4 border-b border-default">
              <div class="flex items-center gap-3">
                <USkeleton class="h-10 w-10 rounded-lg" />
                <div class="space-y-1">
                  <USkeleton class="h-5 w-24" />
                  <USkeleton class="h-4 w-32" />
                </div>
              </div>
            </div>
            <div class="aspect-video bg-muted">
              <div class="w-full h-full flex items-center justify-center">
                <USkeleton class="h-16 w-16 rounded-full" />
              </div>
            </div>
          </div>

          <!-- Content Skeleton -->
          <div
            class="bg-elevated rounded-xl border border-default overflow-hidden"
          >
            <div class="p-6 border-b border-default">
              <div class="flex items-center justify-between">
                <USkeleton class="h-6 w-32" />
                <USkeleton class="h-4 w-20" />
              </div>
            </div>
            <div class="p-6 lg:p-8 space-y-4">
              <USkeleton class="h-4 w-full" />
              <USkeleton class="h-4 w-5/6" />
              <USkeleton class="h-4 w-4/5" />
              <USkeleton class="h-4 w-full" />
              <USkeleton class="h-4 w-3/4" />
              <USkeleton class="h-4 w-full" />
              <USkeleton class="h-4 w-2/3" />
            </div>
          </div>

          <!-- Materials Skeleton -->
          <div
            class="bg-elevated rounded-xl border border-default overflow-hidden"
          >
            <div class="p-6 border-b border-default">
              <div class="flex items-center gap-3">
                <USkeleton class="h-10 w-10 rounded-lg" />
                <div class="space-y-1">
                  <USkeleton class="h-5 w-28" />
                  <USkeleton class="h-4 w-16" />
                </div>
              </div>
            </div>
            <div class="divide-y divide-default">
              <div v-for="i in 3" :key="i" class="p-4 flex items-center gap-4">
                <USkeleton class="h-12 w-12 rounded-lg" />
                <div class="flex-1 space-y-2">
                  <USkeleton class="h-4 w-3/4" />
                  <USkeleton class="h-3 w-1/2" />
                </div>
                <USkeleton class="h-8 w-20 rounded" />
              </div>
            </div>
          </div>

          <!-- Navigation Footer Skeleton -->
          <div class="bg-elevated rounded-xl border border-default p-6">
            <div
              class="flex flex-col sm:flex-row items-center justify-between gap-4"
            >
              <USkeleton class="h-10 w-32" />
              <USkeleton class="h-10 w-36" />
              <USkeleton class="h-10 w-28" />
            </div>
          </div>
        </div>

        <!-- Sidebar Skeleton -->
        <aside class="lg:col-span-4 space-y-6">
          <!-- Course Progress Card Skeleton -->
          <div
            class="bg-elevated rounded-xl border border-default overflow-hidden"
          >
            <div class="p-4 border-b border-default">
              <div class="flex items-start gap-3">
                <USkeleton class="h-12 w-12 rounded-lg" />
                <div class="flex-1 space-y-2">
                  <USkeleton class="h-4 w-3/4" />
                  <USkeleton class="h-3 w-1/2" />
                </div>
              </div>
            </div>
            <div class="p-4 space-y-3">
              <div class="flex items-center justify-between">
                <USkeleton class="h-4 w-24" />
                <USkeleton class="h-4 w-12" />
              </div>
              <USkeleton class="h-2 w-full rounded-full" />
              <div class="grid grid-cols-2 gap-4">
                <div class="text-center p-3 bg-muted/30 rounded-lg space-y-2">
                  <USkeleton class="h-6 w-8 mx-auto" />
                  <USkeleton class="h-3 w-16 mx-auto" />
                </div>
                <div class="text-center p-3 bg-muted/30 rounded-lg space-y-2">
                  <USkeleton class="h-6 w-8 mx-auto" />
                  <USkeleton class="h-3 w-16 mx-auto" />
                </div>
              </div>
            </div>
          </div>

          <!-- Lessons List Skeleton -->
          <div
            class="bg-elevated rounded-xl border border-default overflow-hidden"
          >
            <div
              class="p-4 border-b border-default flex items-center justify-between"
            >
              <USkeleton class="h-5 w-32" />
              <USkeleton class="h-6 w-16 rounded-full" />
            </div>
            <nav class="divide-y divide-default">
              <div v-for="i in 5" :key="i" class="flex items-center gap-3 p-3">
                <USkeleton class="h-8 w-8 rounded-full" />
                <div class="flex-1 space-y-1">
                  <USkeleton class="h-4 w-3/4" />
                  <USkeleton class="h-3 w-1/2" />
                </div>
              </div>
            </nav>
          </div>

          <!-- Assignments Skeleton -->
          <div
            class="bg-elevated rounded-xl border border-default overflow-hidden"
          >
            <div class="p-4 border-b border-default">
              <div class="flex items-center gap-3">
                <USkeleton class="h-10 w-10 rounded-lg" />
                <div class="space-y-1">
                  <USkeleton class="h-5 w-20" />
                  <USkeleton class="h-4 w-16" />
                </div>
              </div>
            </div>
            <div class="p-4 space-y-3">
              <USkeleton class="h-4 w-full" />
              <USkeleton class="h-4 w-3/4" />
              <USkeleton class="h-10 w-full rounded" />
            </div>
          </div>
        </aside>
      </div>
    </UContainer>
  </div>
</template>
