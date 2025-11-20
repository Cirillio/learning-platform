<script lang="ts" setup>
import type { FilterOption } from "~/types";

interface Props {
  search: string;
  category?: string;
  difficulty?: string;
  ordering?: string;
  categoryOptions: FilterOption[];
  difficultyOptions: FilterOption[];
  orderingOptions: FilterOption[];
  isLoading?: boolean;
}

interface Emits {
  (
    e: "apply",
    filters: {
      search: string;
      category?: string;
      difficulty?: string;
      ordering?: string;
    }
  ): void;
  (e: "reset"): void;
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false,
});

const emit = defineEmits<Emits>();

// Локальное состояние фильтров (черновики)
const localSearch = ref<string>(props.search);
const localCategory = ref<string | undefined>(props.category);
const localDifficulty = ref<string | undefined>(props.difficulty);
const localOrdering = ref<string | undefined>(props.ordering);

const categoryOptionsWithDefault = computed(() => {
  return [{ label: "Все категории", value: undefined }, ...props.categoryOptions];
});

const difficultyOptionsWithDefault = computed(() => {
  return [{ label: "Любая сложность", value: undefined }, ...props.difficultyOptions];
});

// Синхронизация с входящими props при их изменении
const unwatchSearch = watch(
  () => props.search,
  (newValue) => {
    localSearch.value = newValue;
  }
);

const unwatchCategory = watch(
  () => props.category,
  (newValue) => {
    localCategory.value = newValue;
  }
);

const unwatchDifficulty = watch(
  () => props.difficulty,
  (newValue) => {
    localDifficulty.value = newValue;
  }
);

const unwatchOrdering = watch(
  () => props.ordering,
  (newValue) => {
    localOrdering.value = newValue;
  }
);

// Очистка watch при размонтировании компонента
onUnmounted(() => {
  unwatchSearch();
  unwatchCategory();
  unwatchDifficulty();
  unwatchOrdering();
});

// Проверка, изменились ли фильтры
const hasChanges = computed(() => {
  return (
    localSearch.value !== props.search ||
    localCategory.value !== props.category ||
    localDifficulty.value !== props.difficulty ||
    localOrdering.value !== props.ordering
  );
});

// Применение фильтров
function applyFilters(): void {
  emit("apply", {
    search: localSearch.value,
    category: localCategory.value,
    difficulty: localDifficulty.value,
    ordering: localOrdering.value,
  });
}

// Очистка фильтров
function clearFilters(): void {
  emit("reset");
}
</script>

<template>
  <div class="space-y-4">
    <!-- Поля фильтров -->
    <div class="flex gap-4 items-center">
      <UInput
        v-model="localSearch"
        icon="i-heroicons-magnifying-glass-20-solid"
        placeholder="Поиск по названию..."
        size="lg"
        :disabled="isLoading"
        :ui="{
          root: 'flex-1',
          base: '!px-10',
        }"
        @keyup.enter="applyFilters"
      />

      <div class="flex gap-4 flex-1">
        <USelectMenu
          v-model="localCategory"
          :items="categoryOptionsWithDefault"
          value-key="value"
          label-key="label"
          placeholder="Категория"
          size="lg"
          clearable
          :disabled="isLoading"
          class="flex-1"
        />

        <USelectMenu
          v-model="localDifficulty"
          :items="difficultyOptionsWithDefault"
          value-key="value"
          label-key="label"
          placeholder="Сложность"
          size="lg"
          clearable
          :disabled="isLoading"
          class="flex-1"
        />
      </div>
    </div>

    <!-- Кнопки действий -->
    <div class="flex gap-3 justify-end">
      <USelectMenu
        v-model="localOrdering"
        :items="orderingOptions"
        value-key="value"
        label-key="label"
        placeholder="Сортировка"
        size="lg"
        :disabled="isLoading"
        class="flex-1"
      />

      <UButton
        label="Очистить"
        icon="i-heroicons-trash"
        size="lg"
        color="error"
        variant="outline"
        :disabled="isLoading || hasChanges"
        @click="clearFilters"
      />

      <UButton
        label="Применить"
        icon="i-heroicons-check"
        size="lg"
        color="primary"
        :disabled="isLoading || !hasChanges"
        @click="applyFilters"
      />
    </div>
  </div>
</template>
