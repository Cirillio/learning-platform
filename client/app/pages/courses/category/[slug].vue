<script lang="ts" setup>
import { useIntersectionObserver } from "@vueuse/core";
import type { CourseFiltersResponse } from "~/types";
import {
  COURSE_PAGE_SIZE_DEFAULT,
  COURSE_ORDERING_DEFAULT,
} from "~/constants/courseFilters";

const route = useRoute();
const categorySlug = route.params.slug as string;
const PAGE_SIZE = COURSE_PAGE_SIZE_DEFAULT;

const { isAuthenticated, isStudent } = useAuthStore();
const { api } = useApi();
const { getCourses, enrollToCourse, getCategory } = useCourses();

// Fetch Category Details
const { data: category, error: categoryError } = await getCategory(
  categorySlug
);

if (categoryError.value || !category.value) {
  throw createError({
    statusCode: 404,
    statusMessage: "Category not found",
  });
}

// Fetch Filter Options (we still need difficulty/ordering)
const { data: filterOptions } = await useAsyncData<CourseFiltersResponse>(
  "course-filter-options",
  () =>
    api("/courses/filters", {
      method: "GET",
    })
);

const {
  difficultyOptions,
  orderingOptions,
  searchValue,
  selectedDifficulty,
  selectedOrdering,
  currentPage,
  apiFilters,
  updatePage,
  updateSearch,
  updateOrdering,
  applyFilters,
  resetFilters,
} = useCourseFilters({
  pageSize: PAGE_SIZE,
  defaultOrdering: COURSE_ORDERING_DEFAULT,
  filterOptions,
});

// Override category in filters
const categoryApiFilters = computed(() => ({
  ...apiFilters.value,
  category: categorySlug,
}));

const {
  data: coursesResponse,
  pending: coursesPending,
  error: coursesError,
} = await getCourses(categoryApiFilters);

const totalItems = computed(() => coursesResponse.value?.count || 0);
const courses = computed(() => coursesResponse.value?.results || []);

const { isEnrolled, isHydrated } = useStudentCourses();

// Local state for search input
const localSearch = ref(searchValue.value);

// Sync local search with URL/Computed
watch(searchValue, (val) => {
  if (val !== localSearch.value) {
    localSearch.value = val;
  }
});

function onSearch() {
  updateSearch(localSearch.value);
}

function clearSearch() {
  localSearch.value = "";
  onSearch();
}

const sentinelRef = ref<HTMLElement | null>(null);
const isStuck = ref(false);

useIntersectionObserver(
  sentinelRef,
  (entries) => {
    const entry = entries[0];
    if (!entry) return;
    isStuck.value = !entry.isIntersecting && entry.boundingClientRect.top < 0;
  },
  { threshold: 0 }
);
</script>

<template>
  <div class="bg-default">
    <CoursesHero
      :title="category?.name || 'Категория'"
      :description="category?.description"
      :image="category?.icon"
    >
      <!-- Search -->
      <div class="flex w-full max-w-lg gap-4 items-center">
        <UInput
          v-model="localSearch"
          leading-icon="i-heroicons-magnifying-glass-20-solid"
          :trailing="false"
          placeholder="Поиск курсов в категории..."
          :disabled="coursesPending"
          class="w-full shadow-md"
          size="xl"
          variant="subtle"
          @keyup.enter="onSearch"
        >
          <template #trailing>
            <UButton
              v-if="localSearch !== ''"
              color="neutral"
              variant="link"
              icon="i-heroicons-x-mark-20-solid"
              :padded="false"
              @click="clearSearch"
            />
          </template>
        </UInput>
        <UButton
          label="Найти"
          color="primary"
          size="xl"
          class="shadow-md"
          :disabled="coursesPending"
          @click="onSearch"
        />
      </div>
    </CoursesHero>

    <!-- Toolbar -->
    <LayoutContainer
      class="relative z-10! sticky-toolbar shadow-xs border-b border-muted bg-default backdrop-blur-xl transition-all duration-300 ease-in-out"
      :class="[isStuck ? 'py-2 bg-default/90' : 'py-6']"
    >
      <div
        ref="sentinelRef"
        class="filters-sentinel invisible absolute -top-2 left-0 right-0 bg-primary z-60 h-px"
      ></div>

      <!-- Note: We don't pass category options here to hide the category selector or we could pass just this category -->
      <CoursesCatalogToolbar
        :difficulty="selectedDifficulty?.value"
        :ordering="selectedOrdering?.value"
        :category-options="[]"
        :difficulty-options="difficultyOptions"
        :ordering-options="orderingOptions"
        :is-loading="coursesPending"
        hide-category
        @update:difficulty="
            (val: any) =>
              applyFilters({ difficulty: val })
          "
        @update:ordering="updateOrdering"
        @reset="resetFilters"
      />
    </LayoutContainer>

    <LayoutContainer class="mt-8">
      <!-- Курсы -->
      <CoursesCatalogCardGrid v-if="courses.length > 0" :courses="courses">
        <CoursesCatalogCard
          v-for="course in courses"
          :key="course.id"
          :course="course"
          :can-enroll="isStudent && isAuthenticated"
          :enrolled="isEnrolled(course)"
          :pending="!isHydrated"
          v-on:enroll="() => enrollToCourse(course.slug)"
        />
      </CoursesCatalogCardGrid>

      <div
        v-else-if="!coursesPending"
        class="text-center py-12 text-neutral-500"
      >
        Курсы в этой категории не найдены
      </div>

      <!-- Пагинация -->
      <div
        v-if="!coursesPending && totalItems > PAGE_SIZE"
        class="mt-8 mx-auto text-dimmed text-sm w-full px-2 items-center flex justify-between"
      >
        <span
          >Показано:
          {{
            1 +
            (currentPage - 1) * PAGE_SIZE +
            "-" +
            Math.min(currentPage * PAGE_SIZE, totalItems)
          }}
        </span>

        <UPagination
          variant="outline"
          color="neutral"
          :active-color="'secondary'"
          active-variant="subtle"
          :page="currentPage"
          :total="totalItems"
          :items-per-page="PAGE_SIZE"
          @update:page="updatePage"
          :ui="{
            item: 'cursor-pointer',
          }"
        />

        <span>Всего: {{ totalItems }} </span>
      </div>
    </LayoutContainer>
    <USeparator class="mt-8" />
  </div>
</template>

<style>
.sticky-toolbar {
  position: sticky;
  top: calc((var(--header-el-height, 49px) - 0px));
  z-index: 80;
}

.filters-sentinel {
  transform: translateY(calc((var(--header-el-height, 49px)) * -1));
}
</style>
