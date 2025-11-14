<script setup lang="ts">
import { loginSchema, type LoginForm } from "~/schemas/auth.schema";
import type { FormSubmitEvent } from "#ui/types";

const emit = defineEmits<{
  submit: [credentials: LoginForm];
}>();

const props = defineProps<{
  isLoading?: boolean;
}>();

// Form state
const state = reactive({
  username: "",
  password: "",
  remember: false,
} as LoginForm);

// Handle form submission with validation
const onSubmit = async (event: FormSubmitEvent<LoginForm>): Promise<void> => {
  emit("submit", event.data);
};
</script>

<template>
  <UForm
    class="flex flex-col mt-8 gap-8 w-full"
    :schema="loginSchema"
    :state="state"
    @submit="onSubmit"
    :validate-on="['change']"
  >
    <UFormField
      label="Логин"
      name="username"
      :ui="{
        label: 'text-lg font-semibold',
      }"
    >
      <UInput
        color="primary"
        v-model="state.username"
        type="text"
        placeholder="Логин или почта"
        class="w-full"
        :ui="{
          base: 'text-xl py-2 px-4',
        }"
      />
    </UFormField>

    <UFormField
      label="Пароль"
      name="password"
      :ui="{
        label: 'text-lg font-semibold',
      }"
    >
      <UInput
        v-model="state.password"
        type="password"
        placeholder="********"
        class="w-full"
        :ui="{
          base: 'text-xl py-2 px-4',
        }"
      />
    </UFormField>

    <UFormField
      name="remember"
      :ui="{
        label: 'text-lg font-medium',
      }"
    >
      <UCheckbox
        size="lg"
        v-model="state.remember"
        label="Оставаться в системе (30 дней)"
        class="*:text-base items-center"
        :ui="{
          label: 'cursor-pointer',
        }"
      />
    </UFormField>

    <UButton
      type="submit"
      label="Войти"
      block
      :loading="props.isLoading"
      size="lg"
      class="text-base"
    />
  </UForm>
</template>
