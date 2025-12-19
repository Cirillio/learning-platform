<!-- pages/courses/all.vue -->
<script lang="ts" setup>
import { useIntersectionObserver } from "@vueuse/core";
import type { CoursesResponse, FiltersResponse, CourseFilters } from "~/types";
import {
  COURSE_PAGE_SIZE_DEFAULT,
  COURSE_ORDERING_DEFAULT,
} from "~/constants/courseFilters";
import { coursesService } from "~/services";
const PAGE_SIZE = COURSE_PAGE_SIZE_DEFAULT;

const { isAuthenticated, isStudent } = useAuthStore();
const coursesApi = coursesService();

const { get } = useApi();

// 1. Load filter options (Client-side only, lazy)
const {
  data: filterOptions,
  pending: filterOptionsPending,
  error: filterOptionsError,
} = useAsyncData<FiltersResponse>(
  "course-filter-options",
  () => get("/courses/filters"),
  {
    server: false,
    lazy: true,
  }
);

// 2. Initialize filters logic
const { filters, apiParams, setFilter, resetFilters } = useCourseFilters();

// 3. Load courses (SSR friendly, reactive to filters)
const {
  data: coursesResponse,
  pending: coursesPending,
  error: coursesError,
} = await useAsyncData<CoursesResponse>(
  () => `courses-${JSON.stringify(apiParams.value)}`, // Unique key based on params
  () => coursesApi.getCourses(apiParams.value),
  {
    watch: [apiParams], // Re-fetch when filters change
  }
);

const totalItems = computed(() => coursesResponse.value?.count || 0);
const courses = computed(() => coursesResponse.value?.results || []);

// 4. Computed options for UI
const getOptions = (key: string) =>
  computed(
    () =>
      filterOptions.value?.filters.find((f) => f.value === key)?.values || []
  );

const categoryOptions = getOptions("category");
const difficultyOptions = getOptions("difficulty");
const orderingOptions = getOptions("ordering");

const {
  isEnrolled,
  pending: studentPending,
  isHydrated,
  refresh: refreshStudentCourses,
} = useStudentCourses();

// Local state for search input (manual trigger)
const localSearch = ref(filters.search || "");

// Sync local search if filters change externally (e.g. URL)
watch(
  () => filters.search,
  (val) => {
    localSearch.value = val || "";
  }
);

function onSearch() {
  setFilter("search", localSearch.value);
}

function clearSearch() {
  localSearch.value = "";
  onSearch();
}

async function handleEnroll(slug: string) {
  try {
    await coursesApi.enrollToCourse(slug);
    await refreshStudentCourses();
  } catch (e) {
    console.error("Failed to enroll", e);
  }
}

const sentinelRef = ref<HTMLElement | null>(null);
const isStuck = ref(false);

useIntersectionObserver(
  sentinelRef,
  (entries) => {
    const entry = entries[0];
    // TypeScript требует гарантии, что entry существует
    if (!entry) return;

    isStuck.value = !entry.isIntersecting && entry.boundingClientRect.top < 0;
  },
  { threshold: 0 }
);
</script>

<template>
  <div class="bg-default">
    <CoursesHero
      title="Каталог курсов"
      description="Изучайте новые навыки с нашими профессиональными курсами."
    >
      <!-- Search -->
      <div class="flex w-full max-w-lg gap-2 items-center">
        <UInput
          v-model="localSearch"
          leading-icon="i-heroicons-magnifying-glass-20-solid"
          :trailing="false"
          placeholder="Поиск курсов..."
          :disabled="coursesPending"
          class="w-full shadow-md opacity-75 hover:opacity-100 focus-within:opacity-100 transition-opacity duration-300"
          size="lg"
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
          size="lg"
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
      <CoursesCatalogToolbar
        v-if="filterOptions"
        :category="filters.category"
        :difficulty="filters.difficulty"
        :ordering="filters.ordering"
        :category-options="categoryOptions"
        :difficulty-options="difficultyOptions"
        :ordering-options="orderingOptions"
        :is-loading="coursesPending"
        @update:category="(val) => setFilter('category', val)"
        @update:difficulty="(val) => setFilter('difficulty', val)"
        @update:ordering="(val) => setFilter('ordering', val)"
        @reset="resetFilters"
      />
      <div v-else class="flex gap-2">
        <USkeleton class="size-9" />
        <div class="flex items-center flex-wrap gap-2 w-full">
          <USkeleton class="flex-1 h-9 w-full" />
          <USkeleton class="flex-1 h-9 w-full" />
          <USkeleton class="flex-1 h-9 w-full" />
        </div>
      </div>
    </LayoutContainer>

    <LayoutContainer class="mt-2">
      <!-- Курсы -->
      <CoursesCatalogCardGrid v-if="courses.length > 0" :courses="courses">
        <CoursesCatalogCard
          v-for="course in courses"
          :key="course.id"
          :course="course"
          :can-enroll="isStudent && isAuthenticated"
          :enrolled="isEnrolled(course)"
          :pending="!isHydrated"
          @enroll="handleEnroll(course.slug)"
        />
      </CoursesCatalogCardGrid>

      <!-- TODO: Courses card skeletons -->

      <div
        v-else-if="!coursesPending"
        class="text-center py-12 text-base text-neutral-500"
      >
        Курсы не найдены
      </div>

      <!-- Пагинация -->
      <div
        v-if="!coursesPending && totalItems > PAGE_SIZE"
        class="mt-2 mx-auto text-base text-dimmed w-full px-2 items-center flex justify-between"
      >
        <span
          >Показано:
          {{
            1 +
            (filters.page - 1) * PAGE_SIZE +
            "-" +
            Math.min(filters.page * PAGE_SIZE, totalItems)
          }}
        </span>

        <UPagination
          variant="outline"
          color="neutral"
          :active-color="'secondary'"
          active-variant="subtle"
          :page="filters.page"
          :total="totalItems"
          :items-per-page="PAGE_SIZE"
          @update:page="(val) => setFilter('page', val)"
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
