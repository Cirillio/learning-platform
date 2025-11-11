<script setup lang="ts">
// Props для настройки скелетона
interface Props {
  /**
   * Количество строк текста
   */
  lines?: number;
  /**
   * Высота каждой строки
   */
  lineHeight?: "sm" | "md" | "lg";
  /**
   * Показывать аватар
   */
  showAvatar?: boolean;
  /**
   * Показывать действие (кнопку)
   */
  showAction?: boolean;
  /**
   * Ширина последней строки (для имитации неполного текста)
   */
  lastLineWidth?: string;
}

const props = withDefaults(defineProps<Props>(), {
  lines: 3,
  lineHeight: "md",
  showAvatar: false,
  showAction: false,
  lastLineWidth: "4/6",
});

// Вычисление высоты строк
const lineHeights = {
  sm: "h-3",
  md: "h-4",
  lg: "h-5",
};
</script>

<template>
  <div class="space-y-3">
    <!-- Аватар -->
    <div v-if="showAvatar" class="flex items-center gap-3">
      <USkeleton class="size-10 rounded-full" />
      <div class="space-y-2 flex-1">
        <USkeleton :class="lineHeights[lineHeight]" class="w-32" />
        <USkeleton :class="lineHeights[lineHeight]" class="w-24" />
      </div>
    </div>

    <!-- Строки текста -->
    <div class="space-y-2">
      <USkeleton
        v-for="n in lines"
        :key="n"
        :class="[
          lineHeights[lineHeight],
          {
            [lastLineWidth]: n === lines && lines > 1,
            'w-full': n !== lines || lines === 1,
          },
        ]"
      />
    </div>

    <!-- Действие -->
    <div v-if="showAction" class="pt-2">
      <USkeleton class="h-8 w-24" />
    </div>
  </div>
</template>
