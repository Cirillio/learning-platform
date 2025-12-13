<script setup lang="ts">
import { useAuthService, useCoursesService } from "~/services";
import type { User, CoursesResponse } from "~/types";

definePageMeta({
  middleware: ["auth", "profile-redirect"],
});

const toast = useToast();

const authService = useAuthService();
const coursesService = useCoursesService();
const { logout, isLoading, user } = useAuth();

// --- Data Fetching ---
// Используем данные из стора, которые уже загружены middleware
// Если данных нет (например, при прямом заходе на страницу без SSR), делаем запрос
const { data: profile, pending: profilePending } = await useAsyncData<User>(
  "user-profile",
  async () => {
    // Оптимизация: на сервере данные уже загружены middleware (полный профиль)
    if (import.meta.server && user.value) {
      return user.value;
    }
    // На клиенте загружаем свежие данные, чтобы гарантировать наличие всех полей профиля
    return authService.fetchUser();
  }
);

const { data: coursesResponse, pending: coursesPending } =
  await useAsyncData<CoursesResponse>(
    "my-courses",
    () => coursesService.getMyCourses(),
    {
      lazy: true,
      server: false,
    }
  );

const myCourses = computed(() => coursesResponse.value?.results || []);

const handleUnEnroll = async (courseSlug: string) => {
  console.log("Unenrolling from course:", courseSlug);
  await coursesService
    .unenrollFromCourse(courseSlug)
    .then(async (res) => {
      toast.add({
        title: "Вы отписаны от курса",
        color: "success",
        icon: "i-lucide-check",
      });
      refreshNuxtData("my-courses");
    })
    .catch((unEnrollError) => {
      toast.add({
        title: "Ошибка отписки от курса",
        description:
          unEnrollError.data?.detail || "Не удалось отписаться от курса",
        color: "error",
        icon: "i-lucide-circle-alert",
      });
    });
};

const handleLogout = async () => {
  try {
    await logout();
    navigateTo("/");
  } catch (error) {
    toast.add({
      title: "Ошибка выхода",
      description: "Не удалось выйти из аккаунта",
      color: "error",
      icon: "i-lucide-circle-alert",
    });
  }
};
</script>

<template>
  <div class="h-full w-full flex flex-1 bg-default py-2">
    <LayoutContainer class="w-full">
      <div v-if="profilePending" class="flex justify-center">
        <UIcon
          name="i-heroicons-arrow-path"
          class="animate-spin size-10 text-primary-500"
        />
      </div>

      <div v-else-if="profile" class="mx-auto flex-col flex gap-2">
        <div class="flex flex-col gap-2">
          <!-- Header -->
          <ProfileHeader :profile="profile" @logout="handleLogout" />
        </div>
        <!-- Блок курсов -->
        <Transition name="fade" mode="out-in">
          <!-- Скелетон всего блока при загрузке -->
          <UCard v-if="!coursesResponse || coursesPending">
            <div class="space-y-4">
              <USkeleton class="h-8 w-48" />
              <div class="flex gap-2">
                <USkeleton class="h-96 flex-1" />
                <USkeleton class="h-96 flex-1" />
                <USkeleton class="h-96 flex-1" />
              </div>
              <USkeleton class="h-8 w-full mt-12" />
            </div>
          </UCard>

          <!-- Карточки курсов если они есть -->
          <UCard
            class="bg-muted/25"
            v-else-if="myCourses.length > 0 && !coursesPending"
          >
            <ProfileCoursesList>
              <CoursesCatalogCard
                v-for="(course, index) in myCourses"
                :key="course.id"
                :pending="coursesPending"
                :course="course"
                :can-enroll="false"
                :can-un-enroll="true"
                :style="{ '--stagger-delay': `${index * 100}ms` }"
                @un-enroll="handleUnEnroll"
              />
              <UButton
                variant="soft"
                color="neutral"
                label="Искать ещё курсы"
                size="xl"
                to="/courses"
                class="justify-center col-span-full mt-4 text-lg"
              />
            </ProfileCoursesList>
          </UCard>

          <!-- Alert если курсов нет -->
          <UAlert
            v-else-if="!coursesPending && coursesResponse?.count === 0"
            title="Нет активных курсов"
            description="Вы еще не записались ни на один курс."
            color="neutral"
            variant="subtle"
            :ui="{
              root: 'p-6 ring-default bg-muted/25',
              title: 'text-2xl font-bold text-error',
              description: 'text-base font-semibold',
            }"
            :actions="[
              {
                label: 'Каталог курсов',
                to: '/courses',
                variant: 'solid',
                color: 'primary',
                size: 'lg',
              },
            ]"
          />
        </Transition>
      </div>
    </LayoutContainer>
  </div>
</template>

<style scoped>
/* Анимация появления скелетона */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Анимация появления карточек с задержкой */
.stagger-enter-active {
  transition: all 0.3s ease;
}

.stagger-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.stagger-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.stagger-move {
  transition: all 0.15s ease;
}

/* Задержка для каждой карточки */
.stagger-enter-active > * {
  transition-delay: var(--stagger-delay, 0ms);
}
</style>
