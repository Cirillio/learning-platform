<script setup lang="ts"></script>

<template>
  <div class="space-y-4">
    <h2 class="text-3xl font-bold text-default">Мои курсы</h2>
    <TransitionGroup
      name="stagger"
      tag="div"
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2"
      appear
    >
      <slot />
    </TransitionGroup>
  </div>
</template>
