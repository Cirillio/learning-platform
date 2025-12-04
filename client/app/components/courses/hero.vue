<script setup lang="ts">
defineProps<{
  title: string;
  description?: string;
  image?: string;
}>();
</script>

<template>
  <section
    class="relative shadow-sm z-20 flex border-b border-muted"
    aria-labelledby="hero-title"
  >
    <NuxtImg
      :src="image || '/courses_page_hero.png'"
      class="object-cover object-center w-full h-[386px] lg:h-[576px]"
    />
    <div
      class="absolute top-2/5 md:top-2/5 left-0 right-0 bottom-0 z-10 bg-linear-to-t from-black to-black/0"
    ></div>
    <LayoutContainer
      class="absolute z-20 left-0 right-0 top-0 bottom-0 py-8 md:py-16"
    >
      <div class="flex flex-col gap-6 items-start size-full justify-between">
        <div class="flex max-xl:gap-2 flex-col justify-end h-full w-full">
          <div class="flex w-full flex-col gap-4">
            <div
              class="flex max-w-5xl flex-col text-white justify-between h-full gap-1 md:gap-2"
            >
              <h1
                id="hero-title"
                class="text-3xl md:text-5xl lg:text-7xl text-balance max-md:font-bold font-medium text-shadow-md"
              >
                {{ title }}
              </h1>
              <h2
                v-if="description"
                class="text-base md:text-xl max-md:font-normal font-extralight text-pretty text-shadow-md"
              >
                {{ description }}
              </h2>
            </div>

            <!-- Slot for Search or other actions -->
            <slot />
          </div>
        </div>
      </div>
    </LayoutContainer>
  </section>
</template>
