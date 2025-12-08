<script setup lang="ts">
import { z } from "zod";
import type { FormSubmitEvent } from "#ui/types";
import type { User } from "~/types";

const props = defineProps<{
  profile: User;
}>();

const emit = defineEmits<{
  (e: "cancel"): void;
  (e: "success"): void;
}>();

const { api } = useApi();
const toast = useToast();
const isLoading = ref(false);

const schema = z.object({
  first_name: z.string().min(1, "Имя обязательно"),
  last_name: z.string().min(1, "Фамилия обязательна"),
  email: z
    .string()
    .or(
      z.string().regex(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/, "Некорректный email")
    ),
  bio: z.string().optional(),
  phone: z.string().optional(),
  address: z.string().optional(),
  city: z.string().optional(),
  country: z.string().optional(),
  birth_date: z.string().optional(),
  specialization: z.string().optional(),
});

type Schema = z.output<typeof schema>;

const state = reactive<Schema>({
  first_name: props.profile.first_name,
  last_name: props.profile.last_name,
  email: props.profile.email,
  bio: props.profile.bio || "",
  phone: props.profile.phone || "",
  address: props.profile.address || "",
  city: props.profile.city || "",
  country: props.profile.country || "",
  birth_date: props.profile.birth_date || "",
  specialization: props.profile.specialization || "",
});

async function onSubmit(event: FormSubmitEvent<Schema>) {
  isLoading.value = true;
  try {
    await api("/auth/profile/", {
      method: "PATCH",
      body: event.data,
    });

    toast.add({
      title: "Профиль обновлен",
      color: "success",
    });

    emit("success");
  } catch (error: any) {
    toast.add({
      title: "Ошибка",
      description: error.data?.detail || "Не удалось обновить профиль",
      color: "error",
    });
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <UCard
    @keydown.esc="emit('cancel')"
    :ui="{
      header: 'bg-primary text-white',
    }"
  >
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="font-semibold text-lg">Редактирование профиля</h3>
        <UButton
          icon="i-heroicons-x-mark"
          color="neutral"
          class="text-white hover:text-white/75"
          variant="link"
          @click="emit('cancel')"
        />
      </div>
    </template>

    <UForm
      :schema="schema"
      :state="state"
      class="flex gap-6 flex-col"
      @submit="onSubmit"
    >
      <div class="flex gap-6">
        <section class="flex-1/2 w-full">
          <!-- Основная информация -->
          <USeparator label="Основная информация" />
          <div class="flex flex-col gap-4">
            <div class="grid mt-6 grid-cols-1 md:grid-cols-2 gap-4">
              <UFormField label="Имя" name="first_name" required>
                <UInput v-model="state.first_name" class="w-full" />
              </UFormField>
              <UFormField label="Фамилия" name="last_name" required>
                <UInput v-model="state.last_name" class="w-full" />
              </UFormField>
            </div>

            <UFormField label="Email" name="email" required>
              <UInput v-model="state.email" type="email" class="w-full" />
            </UFormField>

            <UFormField label="О себе" name="bio">
              <UTextarea
                v-model="state.bio"
                :rows="4"
                class="w-full"
                placeholder="Расскажите немного о себе..."
              />
            </UFormField>
          </div>
        </section>

        <section class="flex-1/2 w-full">
          <USeparator label="Контактные данные" />

          <div class="flex mt-6 gap-4">
            <div class="flex flex-1/2 flex-col gap-4">
              <UFormField label="Страна" name="country" class="w-full">
                <UInput
                  class="w-full"
                  v-model="state.country"
                  icon="i-heroicons-globe-alt"
                />
              </UFormField>
              <UFormField label="Город" name="city" class="w-full">
                <UInput
                  class="w-full"
                  v-model="state.city"
                  icon="i-heroicons-building-office-2"
                />
              </UFormField>
              <UFormField label="Адрес" name="address" class="w-full">
                <UInput
                  class="w-full"
                  v-model="state.address"
                  icon="i-heroicons-map-pin"
                />
              </UFormField>
            </div>

            <div class="flex flex-1/2 flex-col gap-4">
              <UFormField label="Телефон" name="phone">
                <UInput
                  v-model="state.phone"
                  icon="i-heroicons-phone"
                  class="w-full"
                />
              </UFormField>
              <UFormField label="Дата рождения" name="birth_date">
                <UInput v-model="state.birth_date" type="date" class="w-full" />
              </UFormField>
            </div>
          </div>
        </section>
      </div>

      <section>
        <USeparator class="mb-6" label="Профессиональное" />

        <UFormField label="Специализация" name="specialization">
          <UInput
            v-model="state.specialization"
            placeholder="Например: Python Developer"
            icon="i-heroicons-briefcase"
          />
        </UFormField>

        <div class="flex justify-end pt-4 gap-3">
          <UButton color="neutral" variant="soft" @click="emit('cancel')">
            Отмена
          </UButton>
          <UButton type="submit" color="primary" :loading="isLoading">
            Сохранить изменения
          </UButton>
        </div>
      </section>
    </UForm>
  </UCard>
</template>
