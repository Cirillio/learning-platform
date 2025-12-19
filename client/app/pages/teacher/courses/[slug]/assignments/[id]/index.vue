<script setup lang="ts">
import { formatDate, formatFileSize } from "~/utils/formatters.util";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Просмотр задания",
});

const {
  courseSlug,
  assignmentId,
  assignment,
  assignmentStatus,
  lesson,
  submissions,
  pendingCount,
  gradedCount,
  lateCount,
  isDueDatePassed,
  handleDelete,
} = useTeacherAssignment();
</script>

<template>
  <div class="space-y-6">
    <!-- Loading -->
    <SkeletonsAssignment v-if="assignmentStatus === 'pending'" />

    <!-- Error -->
    <SharedNotFound
      v-else-if="!assignment"
      title="Задание не найдено"
      :back-to="`/teacher/courses/${courseSlug}/assignments`"
      back-text="К списку заданий"
    />

    <!-- Content -->
    <template v-else>
      <!-- Header -->
      <TeacherAssignmentsHeader
        :assignment="assignment"
        :is-due-date-passed="isDueDatePassed"
        :course-slug="courseSlug"
        @delete="handleDelete"
      />

      <!-- Lesson Info Card -->
      <TeacherAssignmentsLessonCard
        v-if="lesson"
        :lesson="lesson"
        :course-slug="courseSlug"
      />

      <!-- Quick Stats -->
      <TeacherAssignmentsAssignmentStats
        :total-count="submissions.length"
        :pending-count="pendingCount"
        :graded-count="gradedCount"
        :late-count="lateCount"
      />

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Instructions -->
          <UCard>
            <template #header>
              <div class="flex items-center gap-2">
                <UIcon name="i-lucide-file-text" class="size-5 text-primary" />
                <h3 class="font-semibold">Инструкции</h3>
              </div>
            </template>
            <div
              class="prose prose-neutral dark:prose-invert max-w-none whitespace-pre-wrap"
            >
              {{ assignment.instructions || "Инструкции не указаны" }}
            </div>
          </UCard>

          <!-- Files -->
          <TeacherAssignmentsFilesList :files="assignment.files" />

          <!-- Submissions -->
          <TeacherAssignmentsSubmissionsList :submissions="submissions" />
        </div>

        <!-- Sidebar -->
        <TeacherAssignmentsSidebar
          :assignment="assignment"
          :is-due-date-passed="isDueDatePassed"
          :course-slug="courseSlug"
          :lesson="lesson"
        />
      </div>
    </template>
  </div>
</template>
