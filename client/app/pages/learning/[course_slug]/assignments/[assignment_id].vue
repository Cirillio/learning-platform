<script setup lang="ts">
import type { Assignment, SubmissionDetail, Grade } from "~/types";

definePageMeta({
  layout: "learning",
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
  data: submission,
  pending: submissionPending,
  refresh: refreshSubmission,
} = await useAsyncData<SubmissionDetail | null>(
  `submission-${assignmentId.value}`,
  async () => {
    try {
      return await api.get<SubmissionDetail>(
        `/assignments/${assignmentId.value}/my-submission/`
      );
    } catch {
      return null;
    }
  }
);

// Fetch grade (if graded)
const { data: grade, refresh: refreshGrade } = await useAsyncData<Grade | null>(
  `grade-${assignmentId.value}`,
  async () => {
    if (!submission.value || submission.value.status !== "graded") return null;
    try {
      return await api.get<Grade>(`/submissions/${submission.value.id}/grade/`);
    } catch {
      return null;
    }
  },
  { watch: [submission] }
);

// Computed states
const hasSubmission = computed(() => !!submission.value);
const isGraded = computed(() => submission.value?.status === "graded");
const isPending = computed(() => submission.value?.status === "pending");
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

const handleSubmit = async (payload: { content: string; files: File[] }) => {
  if (!assignment.value || !canSubmit.value) return;

  isSubmitting.value = true;

  try {
    const formData = new FormData();
    formData.append("content", payload.content);
    formData.append("assignment", assignmentId.value);

    payload.files.forEach((file, index) => {
      formData.append(`files[${index}]`, file);
    });

    if (hasSubmission.value) {
      await api.fetch(`/submissions/${submission.value!.id}/`, {
        method: "PATCH",
        body: formData,
        headers: { "Content-Type": "multipart/form-data" },
      });
      toast.add({ title: "Ответ обновлён", color: "success" });
    } else {
      await api.fetch("/submissions/", {
        method: "POST",
        body: formData,
        headers: { "Content-Type": "multipart/form-data" },
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
  <div class="p-6 lg:p-8">
    <!-- Loading -->
    <div v-if="assignmentPending" class="max-w-4xl mx-auto space-y-6">
      <USkeleton class="h-10 w-2/3 rounded-lg" />
      <USkeleton class="h-40 w-full rounded-xl" />
      <USkeleton class="h-60 w-full rounded-xl" />
    </div>

    <!-- Error -->
    <div
      v-else-if="assignmentError"
      class="flex flex-col items-center justify-center py-20 gap-4"
    >
      <UIcon name="i-lucide-alert-circle" class="size-16 text-error" />
      <h2 class="text-xl font-semibold text-default">Задание не найдено</h2>
      <UButton :to="`/learning/${courseSlug}/assignments`" color="primary">
        К списку заданий
      </UButton>
    </div>

    <!-- Content -->
    <template v-else-if="assignment">
      <div class="max-w-4xl mx-auto space-y-6">
        <!-- Back Link -->
        <NuxtLink
          :to="`/learning/${courseSlug}/assignments`"
          class="inline-flex items-center gap-2 text-sm text-muted hover:text-default transition-colors"
        >
          <UIcon name="i-lucide-arrow-left" class="size-4" />
          <span>К списку заданий</span>
        </NuxtLink>

        <!-- Assignment Header -->
        <AssignmentsHeader
          :assignment="assignment"
          :grade="grade"
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
          v-if="isGraded && grade"
          :grade="grade"
          :max-score="assignment.max_score"
        />

        <!-- Submission Form -->
        <AssignmentsSubmissionForm
          ref="submissionFormRef"
          :submission="submission"
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
            >
              {{ hasSubmission ? "Обновить ответ" : "Отправить" }}
            </UButton>
          </template>
        </AssignmentsSubmissionForm>
      </div>
    </template>
  </div>
</template>
