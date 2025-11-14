<script setup lang="ts">
import { registerSchema, type RegisterForm } from "~/schemas/auth.schema";
import type { FormSubmitEvent } from "#ui/types";

const emit = defineEmits<{
  submit: [credentials: RegisterForm];
}>();

const props = defineProps<{
  isLoading?: boolean;
}>();

// Form state
const state = reactive({
  username: "",
  email: "",
  password: "",
  password_confirm: "",
  first_name: "",
  last_name: "",
  role: "student" as const,
} as RegisterForm);

// Handle form submission with validation
const onSubmit = async (event: FormSubmitEvent<RegisterForm>): Promise<void> => {
  emit("submit", event.data);
};
</script>

<template>
  <UForm
    class="flex flex-col mt-8 gap-6 w-full"
    :schema="registerSchema"
    :state="state"
    @submit="onSubmit"
    :validate-on="['change']"
  >
    <div class="grid grid-cols-2 gap-4">
      <UFormField
        label="Имя"
        name="first_name"
        :ui="{
          label: 'text-base font-medium',
        }"
      >
        <UInput
          color="primary"
          v-model="state.first_name"
          type="text"
          placeholder="Ваше имя"
          class="w-full"
          :ui="{
            base: 'text-lg py-2 px-3',
          }"
        />
      </UFormField>

      <UFormField
        label="Фамилия"
        name="last_name"
        :ui="{
          label: 'text-base font-medium',
        }"
      >
        <UInput
          v-model="state.last_name"
          type="text"
          placeholder="Ваша фамилия"
          class="w-full"
          :ui="{
            base: 'text-lg py-2 px-3',
          }"
        />
      </UFormField>
    </div>

    <UFormField
      label="Имя пользователя"
      name="username"
      :ui="{
        label: 'text-base font-medium',
      }"
    >
      <UInput
        color="primary"
        v-model="state.username"
        type="text"
        placeholder="Придумайте логин"
        class="w-full"
        :ui="{
          base: 'text-lg py-2 px-3',
        }"
      />
    </UFormField>

    <UFormField
      label="Email"
      name="email"
      :ui="{
        label: 'text-base font-medium',
      }"
    >
      <UInput
        v-model="state.email"
        type="email"
        placeholder="your.email@example.com"
        class="w-full"
        :ui="{
          base: 'text-lg py-2 px-3',
        }"
      />
    </UFormField>

    <UFormField
      label="Пароль"
      name="password"
      :ui="{
        label: 'text-base font-medium',
      }"
    >
      <UInput
        v-model="state.password"
        type="password"
        placeholder="********"
        class="w-full"
        :ui="{
          base: 'text-lg py-2 px-3',
        }"
      />
    </UFormField>

    <UFormField
      label="Подтверждение пароля"
      name="password_confirm"
      :ui="{
        label: 'text-base font-medium',
      }"
    >
      <UInput
        v-model="state.password_confirm"
        type="password"
        placeholder="********"
        class="w-full"
        :ui="{
          base: 'text-lg py-2 px-3',
        }"
      />
    </UFormField>

    <UButton
      type="submit"
      label="Зарегистрироваться"
      block
      :loading="props.isLoading"
      size="lg"
      class="text-base mt-2"
    />
  </UForm>
</template>