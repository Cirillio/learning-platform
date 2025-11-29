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
    console.log({ ...entry });
    // TypeScript требует гарантии, что entry существует
    if (!entry) return;

    isStuck.value = !entry.isIntersecting && entry.boundingClientRect.top < 0;
  },
  { threshold: 0 }
);
</script>

<template>
  <div class="">
    <section
      class="relative shadow-sm z-20 flex border-b border-muted"
      aria-labelledby="hero-title"
    >
      <NuxtImg
        :src="'/courses_page_hero.png'"
        class="object-cover object-center w-full h-[386px] lg:h-[576px]"
      />
      <div
        class="absolute top-2/5 md:top-2/5 left-0 right-0 bottom-0 z-10 bg-linear-to-t from-black to-black/0"
      ></div>
      <LayoutContainer
        class="absolute z-20 left-0 right-0 top-0 bottom-0 py-8 md:py-16"
      >
        <div class="flex flex-col gap-6 items-start size-full justify-between">
          <div class="flex max-xl:gap-2 flex-col justify-end h-full w-full">
            <div class="flex w-full flex-col gap-4">
              <div
                class="flex max-w-5xl flex-col text-white justify-between h-full gap-1 md:gap-2"
              >
                <h1
                  id="hero-title"
                  class="text-3xl md:text-5xl lg:text-7xl text-balance max-md:font-bold font-medium text-shadow-md"
                >
                  Каталог курсов
                </h1>
                <h2
                  class="text-base md:text-xl max-md:font-normal font-extralight text-pretty text-shadow-md"
                >
                  Изучайте новые навыки с нашими профессиональными курсами.
                </h2>
              </div>
              <!-- Search -->
              <div class="flex w-full max-w-lg gap-4 items-center">
                <UInput
                  v-model="localSearch"
                  leading-icon="i-heroicons-magnifying-glass-20-solid"
                  :trailing="false"
                  placeholder="Поиск курсов..."
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
            </div>
          </div>
        </div>
      </LayoutContainer>
    </section>

    <!-- Toolbar -->
    <LayoutContainer
      class="relative z-10! sticky-toolbar shadow-xs border-b border-muted bg-default/90 backdrop-blur-xl transition-all duration-300 ease-in-out"
      :class="[isStuck ? 'py-2' : 'py-6']"
    >
      <div
        ref="sentinelRef"
        class="filters-sentinel invisible absolute -top-2 left-0 right-0 bg-primary z-60 h-px"
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
