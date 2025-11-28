<!-- pages/courses/all.vue -->
<script lang="ts" setup>
import { useIntersectionObserver } from "@vueuse/core";
import type { CourseFiltersResponse } from "~/types";
import {
  COURSE_PAGE_SIZE_DEFAULT,
  COURSE_ORDERING_DEFAULT,
} from "~/constants/courseFilters";
const PAGE_SIZE = COURSE_PAGE_SIZE_DEFAULT;

const { isAuthenticated, isStudent } = useAuthStore();

const { api } = useApi();
const {
  data: filterOptions,
  pending: filterOptionsPending,
  error: filterOptionsError,
} = await useAsyncData<CourseFiltersResponse>("course-filter-options", () =>
  api("/courses/filters", {
    method: "GET",
  })
);

const {
  categoryOptions,
  difficultyOptions,
  orderingOptions,
  searchValue,
  selectedCategory,
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

const { getCourses, enrollToCourse } = useCourses();
const {
  data: coursesResponse,
  pending: coursesPending,
  error: coursesError,
} = await getCourses(apiFilters);

const totalItems = computed(() => coursesResponse.value?.count || 0);
const courses = computed(() => coursesResponse.value?.results || []);

const { isEnrolled, pending: studentPending, isHydrated } = useStudentCourses();

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

watch(
  () => isStuck.value,
  (newValue) => {
    console.log(newValue);
  }
);

useIntersectionObserver(
  sentinelRef,
  (entries) => {
    const entry = entries[0];
    console.log("intersecting");
    // TypeScript требует гарантии, что entry существует
    if (!entry) return;

    isStuck.value = !entry.isIntersecting && entry.boundingClientRect.top < 0;
  },
  { threshold: 0 }
);
</script>

<template>
  <div class="flex flex-col gap-4 py-16">
    <LayoutContainer>
      <div class="flex flex-1 flex-col">
        <!-- Header -->
        <UPageCard
          title="Каталог курсов"
          description="Изучайте новые навыки с нашими профессиональными курсами."
          icon="heroicons:academic-cap"
          orientation="horizontal"
          spotlight
          spotlight-color="primary"
          :ui="{
            root: 'p-6',
            leadingIcon: 'size-8',
            container: ' !items-start flex-col !flex',
            title: 'text-5xl font-bold text-gray-900 dark:text-white',
            description: 'text-gray-500 text-xl dark:text-gray-400',
          }"
        >
          <!-- Search -->
          <div class="flex w-full max-w-md mt-8 gap-4 items-center">
            <UInput
              v-model="localSearch"
              leading-icon="i-heroicons-magnifying-glass-20-solid"
              :trailing="false"
              placeholder="Поиск курсов..."
              :disabled="coursesPending"
              class="w-full"
              size="lg"
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
              label="Поиск"
              color="primary"
              size="lg"
              :disabled="coursesPending"
              @click="onSearch"
            />
          </div>
        </UPageCard>
      </div>
    </LayoutContainer>

    <!-- Toolbar -->
    <LayoutContainer
      class="relative sticky-toolbar border-b border-muted bg-default/90 backdrop-blur-xl transition-all duration-50"
      :class="[isStuck ? 'py-2' : 'py-4']"
    >
      <div
        ref="sentinelRef"
        class="filters-sentinel absolute left-0 invisible max-w-md z-60 h-px"
      ></div>
      <CoursesCatalogToolbar
        :category="selectedCategory?.value"
        :difficulty="selectedDifficulty?.value"
        :ordering="selectedOrdering?.value"
        :category-options="categoryOptions"
        :difficulty-options="difficultyOptions"
        :ordering-options="orderingOptions"
        :is-loading="coursesPending"
        @update:category="
            (val: any) =>
              applyFilters({
                category: val,
                difficulty: selectedDifficulty?.value,
              })
          "
        @update:difficulty="
            (val: any) =>
              applyFilters({ category: selectedCategory?.value, difficulty: val })
          "
        @update:ordering="updateOrdering"
        @reset="resetFilters"
      />
    </LayoutContainer>

    <LayoutContainer>
      <!-- Курсы -->
      <CoursesItemGrid v-if="courses.length > 0" :courses="courses">
        <CoursesItemCard
          v-for="course in courses"
          :key="course.id"
          :course="course"
          :can-enroll="isStudent && isAuthenticated"
          :enrolled="isEnrolled(course)"
          :pending="!isHydrated"
          v-on:enroll="() => enrollToCourse(course.slug)"
        />
      </CoursesItemGrid>

      <!-- TODO: Courses card skeletons -->

      <div v-else-if="!coursesPending" class="text-center py-12 text-gray-500">
        Курсы не найдены
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
          :page="currentPage"
          :total="totalItems"
          :items-per-page="PAGE_SIZE"
          @update:page="updatePage"
          :show-controls="false"
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
  z-index: 30;
}

.filters-sentinel {
  transform: translateY(calc((var(--header-el-height, 49px) + 18px) * -1));
}
</style>
