<script setup lang="ts">
import type {
  Assignment,
  SubmissionDetail,
  Grade,
  PaginatedResponse,
} from "~/types";

definePageMeta({
  layout: "default",
  middleware: ["auth", "enrolled-course"],
});

const route = useRoute();
const toast = useToast();
const courseSlug = computed(() => route.params.course_slug as string);
const assignmentId = computed(() => route.params.assignment_id as string);

const api = useApi();
const submissionFormRef =
  ref<
    InstanceType<
      typeof import("~/components/assignments/submission-form.vue").default
    >
  >();

// Fetch assignment details
const {
  data: assignment,
  pending: assignmentPending,
  error: assignmentError,
} = await useAsyncData<Assignment>(`assignment-${assignmentId.value}`, () =>
  api.get<Assignment>(`/assignments/${assignmentId.value}/`)
);

// Fetch existing submission (if any)
const {
  data: submissionResponse,
  pending: submissionPending,
  refresh: refreshSubmission,
} = await useAsyncData<PaginatedResponse<SubmissionDetail> | null>(
  `submission-${assignmentId.value}`,
  async () => {
    try {
      return await api.get<PaginatedResponse<SubmissionDetail>>(
        `/submissions/?assignment=${assignmentId.value}`
      );
    } catch {
      return null;
    }
  }
);

// Fetch grade (if graded)
const { data: gradeResponse, refresh: refreshGrade } =
  await useAsyncData<PaginatedResponse<Grade> | null>(
    `grade-${assignmentId.value}`,
    async () => {
      if (
        !submissionResponse.value?.results[0] ||
        submissionResponse.value.results[0].status !== "graded"
      )
        return null;
      try {
        return await api.get<PaginatedResponse<Grade>>(`/grades/`, {
          submission: submissionResponse.value.results[0].id,
        });
      } catch {
        return null;
      }
    },
    { watch: [submissionResponse] }
  );

// Computed states
const hasSubmission = computed(() => !!submissionResponse.value?.results[0]);
const isGraded = computed(
  () => submissionResponse.value?.results[0]?.status === "graded"
);
const isPending = computed(
  () => submissionResponse.value?.results[0]?.status === "pending"
);
const canEdit = computed(() => !isGraded.value);

const isOverdue = computed(() => {
  if (!assignment.value?.due_date) return false;
  return new Date(assignment.value.due_date) < new Date();
});

const canSubmit = computed(() => {
  if (!assignment.value) return false;
  if (isOverdue.value && !assignment.value.allow_late_submission) return false;
  return true;
});

// Submission handler
const isSubmitting = ref(false);

const handleSubmit = async (payload: {
  content: string;
  file: File | null;
}) => {
  if (!assignment.value || !canSubmit.value) return;

  isSubmitting.value = true;

  try {
    const formData = new FormData();
    formData.append("content", payload.content);
    formData.append("assignment", assignmentId.value);
    if (payload.file) {
      formData.append("file", payload.file);
    }

    if (hasSubmission.value && submissionResponse.value?.results[0]) {
      await api.fetch(
        `/submissions/${submissionResponse.value.results[0].id}/`,
        {
          method: "PATCH",
          body: formData,
        }
      );
      toast.add({ title: "Ответ обновлён", color: "success" });
    } else {
      await api.fetch("/submissions/", {
        method: "POST",
        body: formData,
      });
      toast.add({
        title: "Задание сдано!",
        description: "Ожидайте проверки преподавателем",
        color: "success",
      });
    }

    submissionFormRef.value?.resetForm();
    await refreshSubmission();
    await refreshGrade();
  } catch (e: unknown) {
    const error = e as { data?: { detail?: string } };
    toast.add({
      title: "Ошибка",
      description: error.data?.detail || "Не удалось отправить ответ",
      color: "error",
    });
  } finally {
    isSubmitting.value = false;
  }
};

// SEO
useHead(() => ({
  title: assignment.value?.title || "Задание",
}));
</script>

<template>
  <LayoutContainer class="space-y-2 bg-default py-6 flex-1">
    <!-- Loading -->
    <div v-if="assignmentPending" class="max-w-4xl mx-auto space-y-2">
      <USkeleton class="h-10 w-2/3 rounded-lg" />
      <USkeleton class="h-40 w-full rounded-xl" />
      <USkeleton class="h-60 w-full rounded-xl" />
    </div>

    <!-- Error -->
    <div
      v-else-if="assignmentError"
      class="flex flex-col items-center justify-center py-20 gap-2"
    >
      <UIcon name="i-lucide-alert-circle" class="size-16 text-error" />
      <h2 class="text-2xl font-bold text-default">Задание не найдено</h2>
      <UButton
        :to="`/learning/${courseSlug}/assignments`"
        color="primary"
        size="lg"
      >
        К списку заданий
      </UButton>
    </div>

    <!-- Content -->
    <template v-else-if="assignment">
      <div class="space-y-2">
        <div class="flex justify-between">
          <!-- Back Link -->
          <NuxtLink
            :to="`/learning/${courseSlug}/assignments`"
            class="inline-flex items-center gap-2 text-base text-muted hover:text-default transition-colors"
          >
            <UIcon name="i-lucide-arrow-left" class="size-4" />
            <span>К списку заданий</span>
          </NuxtLink>

          <NuxtLink
            :to="
              '/learning/' +
              courseSlug +
              '/lessons/' +
              submissionResponse?.results[0]?.lesson_slug
            "
            class="inline-flex items-center gap-2 text-base text-muted hover:text-default transition-colors"
          >
            <UIcon name="heroicons:document-text" class="size-4" />

            На страницу урока
          </NuxtLink>
        </div>

        <!-- Assignment Header -->
        <AssignmentsHeader
          :assignment="assignment"
          :grade="gradeResponse?.results[0]"
          :is-graded="isGraded"
          :is-pending="isPending"
          :is-overdue="isOverdue"
          :has-submission="hasSubmission"
        />

        <!-- Instructions -->
        <AssignmentsInstructionsCard
          v-if="assignment.instructions"
          :instructions="assignment.instructions"
        />

        <!-- Attached Files -->
        <AssignmentsFilesList
          v-if="assignment.files.length > 0"
          :files="assignment.files"
        />

        <!-- Grade Result -->
        <AssignmentsGradeResult
          v-if="
            isGraded &&
            gradeResponse &&
            gradeResponse.results[0] &&
            gradeResponse?.results.length > 0
          "
          :grade="gradeResponse.results[0]"
          :max-score="assignment.max_score"
        />

        <!-- Submission Form -->
        <AssignmentsSubmissionForm
          ref="submissionFormRef"
          :submission="submissionResponse?.results[0]"
          :has-submission="hasSubmission"
          :can-edit="canEdit"
          :can-submit="canSubmit"
          @submit="handleSubmit"
        >
          <template #submit-button>
            <UButton
              type="submit"
              color="primary"
              :loading="isSubmitting"
              icon="i-lucide-send"
              size="lg"
            >
              {{ hasSubmission ? "Обновить ответ" : "Отправить" }}
            </UButton>
          </template>
        </AssignmentsSubmissionForm>
      </div>
    </template>
  </LayoutContainer>
</template>
