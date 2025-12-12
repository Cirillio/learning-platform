<script setup lang="ts">
import type { pageHeader } from "#build/ui";
import { z } from "zod";
import type { User } from "~/types";

const props = defineProps<{
  profile: User | undefined;
  onSubmit: (data: EditSchema) => Promise<void>;
  isLoading: boolean;
  profileLoading: boolean;
  error: string | null;
}>();

const emit = defineEmits<{
  (e: "cancel"): void;
  (e: "success"): void;
}>();

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
  birth_date: z.union([z.string(), z.null()]).optional(),
  specialization: z.string().optional(),
});

export type EditSchema = z.output<typeof schema>;

const state = reactive<EditSchema>({
  first_name: props.profile?.first_name || "",
  last_name: props.profile?.last_name || "",
  email: props.profile?.email || "",
  bio: props.profile?.bio || "",
  phone: props.profile?.phone || "",
  address: props.profile?.address || "",
  city: props.profile?.city || "",
  country: props.profile?.country || "",
  birth_date: props.profile?.birth_date || "",
  specialization: props.profile?.specialization || "",
});
</script>

<template>
  <UForm
    :schema="schema"
    :state="state"
    class="space-y-4"
    @submit="() => props.onSubmit(state)"
  >
    <h2
      class="text-2xl w-fit font-semibold text-highlighted border-b border-default pb-3"
    >
      Личная информация
    </h2>
    <div class="max-w-3xl grid grid-cols-1 md:grid-cols-2 gap-4">
      <UFormField label="First name" name="first_name" required size="xl">
        <UInput
          v-model="state.first_name"
          class="w-full"
          color="neutral"
          variant="soft"
          :disabled="isLoading"
          size="xl"
        />
      </UFormField>

      <UFormField label="Last name" name="last_name" required size="xl">
        <UInput
          v-model="state.last_name"
          class="w-full"
          color="neutral"
          variant="soft"
          :disabled="isLoading"
          size="xl"
        />
      </UFormField>
    </div>

    <UFormField
      label="What best describes your work?"
      size="xl"
      name="specialization"
      help="This will be displayed on your public profile."
      class="max-w-3xl"
    >
      <UInput
        v-model="state.specialization"
        placeholder="e.g. Engineering"
        class="w-full"
        color="neutral"
        :disabled="isLoading"
        variant="soft"
        size="xl"
      />
    </UFormField>

    <UFormField
      label="Bio"
      name="bio"
      size="xl"
      description="What personal preferences should we consider?"
    >
      <UTextarea
        v-model="state.bio"
        :rows="4"
        class="w-full"
        placeholder="Tell us a little bit about yourself..."
        color="neutral"
        variant="soft"
        :disabled="isLoading"
        autoresize
        size="xl"
      />
    </UFormField>

    <UFormField label="Birth Date" name="birth_date" size="xl">
      <UInput
        v-model="state.birth_date"
        type="date"
        color="neutral"
        :disabled="isLoading"
        size="xl"
        variant="soft"
        :ui="{
          base: 'px-4',
        }"
        :max="new Date().toISOString().split('T')[0]"
      />
    </UFormField>

    <USeparator class="my-4" />

    <div class="space-y-2 max-w-2xl">
      <h2
        class="text-2xl w-fit font-semibold text-highlighted border-b border-default pb-3"
      >
        Контактная информация
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <UFormField label="Email" name="email" size="xl">
          <UInput
            v-model="state.email"
            type="email"
            icon="i-lucide-mail"
            :disabled="isLoading"
            color="neutral"
            variant="soft"
            size="xl"
            class="w-full"
          />
        </UFormField>

        <UFormField label="Phone" name="phone" size="xl">
          <UInput
            v-model="state.phone"
            icon="i-lucide-phone"
            color="neutral"
            :disabled="isLoading"
            size="xl"
            variant="soft"
            class="w-full"
          />
        </UFormField>

        <UFormField label="Country" name="country" size="xl">
          <UInput
            v-model="state.country"
            icon="i-lucide-globe"
            :disabled="isLoading"
            color="neutral"
            size="xl"
            variant="soft"
            class="w-full"
          />
        </UFormField>

        <UFormField label="City" name="city" size="xl">
          <UInput
            v-model="state.city"
            icon="i-lucide-building-2"
            :disabled="isLoading"
            color="neutral"
            size="xl"
            variant="soft"
            class="w-full"
          />
        </UFormField>

        <UFormField label="Address" name="address" size="xl">
          <UInput
            v-model="state.address"
            icon="i-lucide-map-pin"
            :disabled="isLoading"
            color="neutral"
            variant="soft"
            size="xl"
            class="w-full"
          />
        </UFormField>
      </div>
    </div>

    <div class="flex items-center gap-3 mt-8">
      <UButton
        type="submit"
        color="primary"
        variant="solid"
        size="xl"
        label="Save profile"
        :loading="isLoading"
        :disabled="profileLoading"
      />

      <UButton
        color="neutral"
        variant="ghost"
        size="xl"
        label="Cancel"
        :disabled="isLoading"
        @click="emit('cancel')"
      />
    </div>
  </UForm>
</template>
