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
  remember_me: false,
} as LoginForm);

// Handle form submission with validation
const onSubmit = async (event: FormSubmitEvent<LoginForm>): Promise<void> => {
  emit("submit", event.data);
};
</script>

<template>
  <UForm
    class="flex flex-col mt-8 gap-4 lg:gap-8 w-full"
    :schema="loginSchema"
    :state="state"
    @submit="onSubmit"
    :validate-on="['change']"
  >
    <UFormField
      label="Логин"
      name="username"
      :ui="{
        label: 'text-base lg:text-lg font-semibold',
      }"
    >
      <UInput
        color="primary"
        v-model="state.username"
        type="text"
        placeholder="Логин или почта"
        class="w-full"
        :ui="{
          base: 'text-base lg:text-xl py-2 px-4',
        }"
      />
    </UFormField>

    <UFormField
      label="Пароль"
      name="password"
      :ui="{
        label: 'text-base lg:text-lg font-semibold',
      }"
    >
      <UInput
        v-model="state.password"
        type="password"
        placeholder="********"
        class="w-full"
        :ui="{
          base: 'text-base lg:text-xl py-2 px-4',
        }"
      />
    </UFormField>

    <UFormField
      name="remember_me"
      :ui="{
        label: 'text-base lg:text-lg font-medium w-fit',
      }"
    >
      <UCheckbox
        size="lg"
        color="secondary"
        v-model="state.remember_me"
        label="Оставаться в системе"
        class="*:text-base items-center w-fit"
        :ui="{
          label: 'cursor-pointer',
        }"
      />
    </UFormField>

    <UButton
      type="submit"
      label="Войти"
      class="w-full md:w-fit justify-center md:text-lg"
      :loading="props.isLoading"
    />
  </UForm>
</template>
