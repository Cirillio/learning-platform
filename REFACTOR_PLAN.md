# REFACTORING PLAN

## Phase 1: Foundation (Types & Utils)
*Goal: Eliminate duplication and establish a single source of truth.*

### 1.1. Unify API Types
- [ ] Create `client/app/types/api.types.ts`:
    - Define generic `PaginatedResponse<T>`.
    - Move `CoursesResponse`, `SubmissionsResponse`, etc., to use this generic.
- [ ] Update `client/app/types/index.ts` to export these new types.

### 1.2. Centralize Utilities
- [ ] Verify `client/app/utils/formatters.util.ts` covers all date/size cases.
- [ ] **Action:** Scan codebase and replace all inline `toLocaleDateString` and file size math with imports from `formatters.util.ts`.

## Phase 2: Feature Refactoring (Priority: Teacher Section)
*Goal: Decompose "God Objects" following strict separation of concerns.*

### 2.1. Feature: Assignment Details
*Target:* `client/app/pages/teacher/courses/[slug]/assignments/[id]/index.vue` (551 lines)
- [ ] **Step 1 (Logic):** Extract data fetching and computed logic to `client/app/composables/use-teacher-assignment.ts`.
- [ ] **Step 2 (UI):** Extract sub-components to `client/app/components/teacher/assignments/`:
    - `assignment-header.vue`
    - `assignment-stats.vue`
    - `assignment-submissions-table.vue` (The largest part)
    - `assignment-info-sidebar.vue`
- [ ] **Step 3 (Cleanup):** Reassemble the page using the new parts.

### 2.2. Feature: Lesson Editor
*Target:* `client/app/pages/teacher/courses/[slug]/lessons/[lesson_slug]/index.vue` (537 lines)
- [ ] **Step 1 (Logic):** Create `client/app/composables/use-lesson-editor.ts`.
- [ ] **Step 2 (UI):** Extract components:
    - `lesson-editor-header.vue`
    - `lesson-content-form.vue`
    - `lesson-materials-manager.vue`

## Phase 3: Composable Cleanup
*Goal: Break down monolithic composables.*

### 3.1. Refactor `useComments.ts` (478 lines)
- [ ] Split into:
    - `use-comments-fetch.ts` (API interaction)
    - `use-comments-state.ts` (Local UI state)
    - `use-comments-actions.ts` (Create/Delete/Update)

### 3.2. Refactor `useLessons.ts` (386 lines)
- [ ] Analyze responsibilities and split by domain (e.g., student view vs teacher management).

## Checklist for Every Change
1.  Does it use global types?
2.  Are utils imported?
3.  Is the file < 200 lines?
4.  Does it follow kebab-case naming?
