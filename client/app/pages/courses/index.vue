<!-- pages/courses/all.vue -->
<script lang="ts" setup>
import {
  COURSE_PAGE_SIZE_DEFAULT,
  COURSE_ORDERING_DEFAULT,
} from "~/constants/courseFilters";
const PAGE_SIZE = COURSE_PAGE_SIZE_DEFAULT;

definePageMeta({
  layout: "courses-catalog",
});

const { isAuthenticated, isStudent } = useAuthStore();

const { api } = useApi();
const { data: filterOptions } = await useAsyncData<
  import("~/types").CourseFiltersResponse
>("course-filter-options", () =>
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
  applyFilters,
  resetFilters,
} = useCourseFilters({
  pageSize: PAGE_SIZE,
  defaultOrdering: COURSE_ORDERING_DEFAULT,
  filterOptions,
});

const { getCourses, enrollToCourse } = useCourses();
const { data: coursesResponse, pending, error: coursesError } = await getCourses(
  apiFilters
);

const totalItems = computed(() => coursesResponse.value?.count || 0);
const courses = computed(() => coursesResponse.value?.results || []);

const { isEnrolled, pending: studentPending, isHydrated } = useStudentCourses();
</script>

<template>
  <UContainer>
    <!-- Фильтры -->
    <CoursesItemFilters
      class="mt-8"
      :search="searchValue"
      :category="selectedCategory?.value"
      :difficulty="selectedDifficulty?.value"
      :ordering="selectedOrdering?.value"
      :category-options="categoryOptions"
      :difficulty-options="difficultyOptions"
      :ordering-options="orderingOptions"
      :is-loading="pending"
      @apply="applyFilters"
      @reset="resetFilters"
    />

    <!-- Курсы -->
    <CoursesItemGrid v-if="courses.length > 0" class="mt-8" :courses="courses">
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

    <!-- Пагинация -->
    <div v-if="!pending && totalItems > PAGE_SIZE" class="mt-8 flex justify-center">
      <UPagination
        :page="currentPage"
        :total="totalItems"
        :items-per-page="PAGE_SIZE"
        @update:page="updatePage"
      />
    </div>
  </UContainer>
</template>
input: "group-hover:border-secondary !text-xl",
