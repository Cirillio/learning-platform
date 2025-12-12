<script setup lang="ts">
interface Props {
  title: string;
  content: string;
  duration?: number;
}

defineProps<Props>();
</script>

<template>
  <article>
    <UCard class="dark:bg-muted/25 bg-muted/75">
      <!-- Content Header -->
      <div class="p-6 border-b border-default">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold text-default">Материал урока</h2>
          <span v-if="duration" class="text-sm text-muted">
            ~{{ duration }} мин на изучение
          </span>
        </div>
      </div>

      <!-- Markdown Content -->
      <div class="p-6 lg:p-8">
        <div
          class="prose prose-neutral dark:prose-invert max-w-none prose-headings:font-semibold prose-headings:text-default prose-p:text-dimmed prose-p:leading-relaxed prose-a:text-primary prose-a:no-underline hover:prose-a:underline prose-code:bg-muted prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-pre:bg-elevated prose-pre:border prose-pre:border-default prose-img:rounded-lg prose-img:shadow-md prose-blockquote:border-l-primary prose-blockquote:bg-muted/50 prose-blockquote:py-1 prose-blockquote:px-4 prose-blockquote:rounded-r"
          v-html="content"
        />
      </div>
    </UCard>
  </article>
</template>
