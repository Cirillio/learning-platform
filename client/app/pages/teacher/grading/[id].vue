<script setup lang="ts">
import { z } from "zod";
import type { SubmissionDetail, Assignment, Grade } from "~/types";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Проверка работы",
});

const route = useRoute();
const router = useRouter();
const api = useApi();
const toast = useToast();

const submissionId = computed(() => route.params.id as string);

// Fetch submission details
const {
  data: submission,
  pending: submissionPending,
  error: submissionError,
  refresh: refreshSubmission,
} = await useAsyncData<SubmissionDetail>(
  `teacher-submission-${submissionId.value}`,
  () => api.get<SubmissionDetail>(`/submissions/${submissionId.value}/`)
);

// Fetch assignment for max_score
const { data: assignment } = await useAsyncData<Assignment | null>(
  `teacher-submission-assignment-${submissionId.value}`,
  async () => {
    if (!submission.value) return null;
    return await api.get<Assignment>(
      `/assignments/${submission.value.assignment}/`
    );
  },
  { watch: [submission] }
);

// Fetch existing grade if graded
const { data: existingGrade, refresh: refreshGrade } =
  await useAsyncData<Grade | null>(
    `teacher-submission-grade-${submissionId.value}`,
    async () => {
      if (!submission.value || submission.value.status !== "graded")
        return null;
      try {
        return await api.get<Grade>(
          `/submissions/${submissionId.value}/grade/`
        );
      } catch {
        return null;
      }
    },
    { watch: [submission] }
  );

// Grade Form
const gradeSchema = z.object({
  score: z.number().min(0, "Оценка не может быть отрицательной"),
  feedback: z.string().max(5000, "Слишком длинный комментарий").optional(),
});

const gradeForm = reactive({
  score: existingGrade.value?.score || 0,
  feedback: existingGrade.value?.feedback || "",
});

const isSubmitting = ref(false);

// Watch for existing grade changes
watch(existingGrade, (grade) => {
  if (grade) {
    gradeForm.score = grade.score;
    gradeForm.feedback = grade.feedback || "";
  }
});

// Computed
const maxScore = computed(() => assignment.value?.max_score || 100);
const isGraded = computed(() => submission.value?.status === "graded");

// Actions
const submitGrade = async () => {
  // Validate
  const result = gradeSchema.safeParse(gradeForm);
  if (!result.success) {
    toast.add({
      title: "Ошибка",
      description: result.error.issues[0]?.message,
      color: "error",
    });
    return;
  }

  if (gradeForm.score > maxScore.value) {
    toast.add({
      title: "Ошибка",
      description: `Оценка не может превышать ${maxScore.value}`,
      color: "error",
    });
    return;
  }

  isSubmitting.value = true;

  try {
    await api.post(`/grades/`, {
      submission: submissionId.value,
      score: gradeForm.score,
      feedback: gradeForm.feedback,
    });

    toast.add({
      title: "Оценка выставлена",
      description: "Работа успешно проверена",
      color: "success",
    });

    await refreshSubmission();
    await refreshGrade();
  } catch (e: any) {
    toast.add({
      title: "Ошибка",
      description: e.data?.detail || "Не удалось выставить оценку",
      color: "error",
    });
  } finally {
    isSubmitting.value = false;
  }
};

// SEO
useHead(() => ({
  title: submission.value
    ? `Проверка: ${submission.value.assignment_title}`
    : "Загрузка...",
}));
</script>

<template>
  <div>
    <!-- Loading -->
    <div v-if="submissionPending" class="space-y-6">
      <USkeleton class="h-10 w-1/3" />
      <USkeleton class="h-64 rounded-xl" />
      <USkeleton class="h-48 rounded-xl" />
    </div>

    <!-- Error -->
    <div v-else-if="submissionError || !submission" class="text-center py-20">
      <UIcon
        name="i-lucide-alert-circle"
        class="size-16 text-error mx-auto mb-4"
      />
      <h2 class="text-xl font-semibold text-default mb-2">Работа не найдена</h2>
      <UButton to="/teacher/grading" color="primary"> К списку работ </UButton>
    </div>

    <!-- Content -->
    <template v-else>
      <!-- Header -->
      <TeacherGradingDetailHeader
        :submission="submission"
        :is-graded="isGraded"
      />

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Student's Answer -->
          <TeacherGradingDetailStudentAnswer :content="submission.content" />

          <!-- Attached Files -->
          <TeacherGradingDetailAttachedFiles :files="submission.files" />
        </div>

        <!-- Grading Panel -->
        <TeacherGradingDetailGradingPanel
          :grade-form="gradeForm"
          :max-score="maxScore"
          :is-graded="isGraded"
          :is-submitting="isSubmitting"
          :existing-grade="existingGrade ?? null"
          @submit="submitGrade"
        />
      </div>
    </template>
  </div>
</template>
