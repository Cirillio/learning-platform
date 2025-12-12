<script lang="ts" setup>
import { onUnmounted } from "vue";
import type { FilterOption } from "~/types";

interface Props {
  category?: string;
  difficulty?: string;
  ordering?: string;
  categoryOptions: FilterOption[];
  difficultyOptions: FilterOption[];
  orderingOptions: FilterOption[];
  isLoading?: boolean;
  hideCategory?: boolean;
}

interface Emits {
  (e: "update:category", value: string | undefined): void;
  (e: "update:difficulty", value: string | undefined): void;
  (e: "update:ordering", value: string | undefined): void;
  (e: "reset"): void;
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false,
  hideCategory: false,
});

const emit = defineEmits<Emits>();

// Options with defaults
const categoryOptionsWithDefault = computed(() => [
  { label: "Все курсы", value: undefined },
  ...props.categoryOptions,
]);

const difficultyOptionsWithDefault = computed(() => [
  { label: "Все уровни", value: undefined },
  ...props.difficultyOptions,
]);

const orderingOptionsWithDefault = computed(() => [
  { label: "По умолчанию", value: undefined },
  ...props.orderingOptions,
]);

// Local state — биндим к VALUE (string | undefined), а не к объектам
const localCategory = ref<string | undefined>(props.category);
const localDifficulty = ref<string | undefined>(props.difficulty);
const localOrdering = ref<string | undefined>(props.ordering);

// Sync from props to local values
const stopWatchCategory = watch(
  () => props.category,
  (val) => {
    localCategory.value = val;
  }
);

const stopWatchDifficulty = watch(
  () => props.difficulty,
  (val) => {
    localDifficulty.value = val;
  }
);

const stopWatchOrdering = watch(
  () => props.ordering,
  (val) => {
    localOrdering.value = val;
  }
);

// Sync from local values to emits
const stopWatchLocalCategory = watch(localCategory, (val) => {
  if (val !== props.category) emit("update:category", val);
});

const stopWatchLocalDifficulty = watch(localDifficulty, (val) => {
  if (val !== props.difficulty) emit("update:difficulty", val);
});

const stopWatchLocalOrdering = watch(localOrdering, (val) => {
  if (val !== props.ordering) emit("update:ordering", val);
});

// Cleanup watchers on unmount
onUnmounted(() => {
  stopWatchCategory();
  stopWatchDifficulty();
  stopWatchOrdering();
  stopWatchLocalCategory();
  stopWatchLocalDifficulty();
  stopWatchLocalOrdering();
});

const hasActiveFilters = computed(() => {
  return !!props.category || !!props.difficulty || !!props.ordering;
});
</script>

<template>
  <div class="flex flex-wrap items-center gap-2 w-full">
    <!-- Reset Button -->
    <UTooltip text="Сбросить фильтры">
      <UButton
        icon="i-heroicons-x-mark"
        :color="isLoading ? 'neutral' : !hasActiveFilters ? 'neutral' : 'error'"
        variant="outline"
        :disabled="isLoading || !hasActiveFilters"
        @click="$emit('reset')"
        size="lg"
        class="shadow-xs"
      />
    </UTooltip>

    <!-- Category -->
    <USelect
      v-if="!hideCategory"
      placeholder="Категория"
      v-model="localCategory"
      :items="categoryOptionsWithDefault"
      class="flex-1"
      color="secondary"
      size="lg"
    />

    <!-- Difficulty -->
    <USelect
      placeholder="Сложность"
      v-model="localDifficulty"
      :items="difficultyOptionsWithDefault"
      class="flex-1"
      color="secondary"
      size="lg"
    />

    <!-- Ordering -->
    <USelect
      placeholder="Сортировка"
      v-model="localOrdering"
      :items="orderingOptionsWithDefault"
      class="flex-1"
      color="secondary"
      size="lg"
    />
  </div>
</template>
