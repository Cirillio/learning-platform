<script lang="ts" setup></script>

<template>
  <div
    v-bind="$attrs"
    class="grid grid-cols-2 lg:grid-cols-3 2xl:grid-cols-3 gap-2"
  >
    <slot />
  </div>
</template>
