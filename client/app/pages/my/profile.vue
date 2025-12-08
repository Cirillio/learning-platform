<script setup lang="ts">
import type { Profile, User } from "~/types";

definePageMeta({
  middleware: ["auth"],
});

const { api } = useApi();
const { logout } = useAuth();
const { setUser } = useAuthStore();
const { getMyCourses } = useCourses();

// --- Data Fetching ---
const {
  data: profile,
  pending: profilePending,
  refresh: refreshProfile,
} = await useAsyncData<User>("user-profile", () =>
  api("/auth/profile/", { method: "GET" })
);

const { data: coursesResponse, pending: coursesPending } = await useAsyncData(
  "my-courses",
  () => getMyCourses()
);

const myCourses = computed(() => coursesResponse.value?.results || []);

// --- Edit Modal ---
const isModalOpen = ref(false);

const handleUpdateSuccess = async () => {
  await refreshProfile();
  setUser(profile.value || null);
  isModalOpen.value = false;
};
</script>

<template>
  <div class="min-h-screen bg-muted py-2">
    <LayoutContainer>
      <div v-if="profilePending" class="flex justify-center">
        <UIcon
          name="i-heroicons-arrow-path"
          class="animate-spin size-10 text-primary-500"
        />
      </div>

      <div v-else-if="profile" class="mx-auto flex-col flex gap-2">
        <div class="flex gap-2">
          <!-- Header -->
          <ProfileHeader
            :profile="profile"
            @edit-success="handleUpdateSuccess"
            @logout="logout"
          />

          <!-- Details Grid (Read Only) -->
          <div class="flex gap-2 w-full flex-1">
            <!-- Left Column: Personal Info & Courses -->
            <ProfileInfoCard :profile="profile" class="flex-2/3" />
            <!-- Right Column: Academic Info -->
            <ProfileAcademicCard :profile="profile" class="flex-1/3" />
          </div>
        </div>
        <div class="flex w-full">
          <ProfileCoursesList
            class="w-2/3"
            :courses="myCourses"
            :pending="coursesPending"
          />
        </div>
      </div>
    </LayoutContainer>
  </div>
</template>
