<script setup lang="ts">
import { useTeacherLesson } from "~/composables/use-teacher-lesson";

definePageMeta({
  layout: "teacher",
  middleware: ["teacher-only"],
  title: "Просмотр урока",
});

const {
  courseSlug,
  lessonSlug,
  lesson,
  lessonStatus,
  assignments,
  submissions,
  submissionsByAssignment,
  pendingSubmissions,
  gradedSubmissions,
  handleDelete,
} = useTeacherLesson();
</script>

<template>
  <div class="space-y-6">
    <!-- Loading -->
    <SkeletonsAssignment v-if="lessonStatus === 'pending'" />

    <!-- Error -->
    <SharedNotFound
      v-else-if="!lesson"
      title="Урок не найден"
      :back-to="`/teacher/courses/${courseSlug}/lessons`"
      back-text="К списку уроков"
    />

    <!-- Content -->
    <template v-else>
      <!-- Header -->
      <TeacherLessonsHeader
        :lesson="lesson"
        :course-slug="courseSlug"
        :assignments-count="assignments.length"
        @delete="handleDelete"
      />

      <!-- Quick Stats -->
      <TeacherLessonsStats
        :assignments-count="assignments.length"
        :pending-count="pendingSubmissions"
        :graded-count="gradedSubmissions"
        :total-submissions="submissions.length"
      />

      <!-- Video -->
      <TeacherLessonsVideoPlayer
        v-if="lesson.video_url"
        :video-url="lesson.video_url"
      />

      <!-- Content -->
      <UCard v-if="lesson.content">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-file-text" class="size-5 text-primary" />
            <h3 class="font-semibold">Содержание урока</h3>
          </div>
        </template>
        <LessonsContentViewer
          :title="lesson.title"
          :content="lesson.content"
          :duration="lesson.duration_minutes"
        />
      </UCard>

      <!-- Materials -->
      <TeacherLessonsMaterialsList :materials="lesson.materials" />

      <!-- Assignments with Submissions -->
      <TeacherLessonsAssignmentsList
        :assignments="assignments"
        :submissions-by-assignment="submissionsByAssignment"
        :course-slug="courseSlug"
        :lesson-slug="lessonSlug"
      />

      <!-- Comments -->
      <ClientOnly>
        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon
                name="i-lucide-message-circle"
                class="size-5 text-primary"
              />
              <h3 class="font-semibold">Комментарии</h3>
            </div>
          </template>
          <CommentsList :lesson-id="lesson.id" />
        </UCard>
      </ClientOnly>
    </template>
  </div>
</template>