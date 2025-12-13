<script lang="ts" setup>
const { user } = useAuthStore();

// Current plan (mock data)
const currentPlan = ref({
  name: "Бесплатный",
  price: 0,
  period: "month",
  features: [
    "Доступ к бесплатным курсам",
    "Базовая поддержка",
    "Сертификаты об окончании",
  ],
});

// Available plans
const plans = [
  {
    name: "Бесплатный",
    price: 0,
    period: "month",
    description: "Для начинающих",
    features: [
      "Доступ к бесплатным курсам",
      "Базовая поддержка",
      "Сертификаты об окончании",
    ],
    current: true,
  },
  {
    name: "Стандарт",
    price: 990,
    period: "month",
    description: "Для активного обучения",
    features: [
      "Все бесплатные курсы",
      "Доступ к премиум-курсам",
      "Приоритетная поддержка",
      "Скачивание материалов",
      "Без рекламы",
    ],
    popular: true,
  },
  {
    name: "Премиум",
    price: 1990,
    period: "month",
    description: "Максимум возможностей",
    features: [
      "Всё из Стандарта",
      "Персональный ментор",
      "Эксклюзивные вебинары",
      "Ранний доступ к курсам",
      "Сертификаты с верификацией",
    ],
  },
];

// Payment history (mock data)
const paymentHistory = ref([
  {
    id: 1,
    date: "2024-01-15",
    amount: 990,
    description: "Подписка Стандарт",
    status: "completed",
  },
  {
    id: 2,
    date: "2023-12-15",
    amount: 990,
    description: "Подписка Стандарт",
    status: "completed",
  },
]);

const formatDate = (date: string) => {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(new Date(date));
};

const formatPrice = (price: number) => {
  return new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "RUB",
    minimumFractionDigits: 0,
  }).format(price);
};

definePageMeta({
  layout: "settings",
});

useHead({
  title: "Оплата и подписка",
});
</script>

<template>
  <div class="space-y-6 max-w-3xl">
    <!-- Page Header -->
    <div class="pb-4 border-b border-default">
      <h2 class="text-xl font-semibold text-default">Оплата и подписка</h2>
      <p class="text-sm text-muted mt-1">
        Управляйте вашей подпиской и способами оплаты
      </p>
    </div>

    <!-- Current Plan -->
    <UCard>
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div
              class="size-10 rounded-lg bg-primary/10 flex items-center justify-center"
            >
              <UIcon name="i-lucide-crown" class="size-5 text-primary" />
            </div>
            <div>
              <h3 class="font-semibold text-default">Текущий план</h3>
              <p class="text-sm text-muted">Ваша активная подписка</p>
            </div>
          </div>
          <UBadge color="success" variant="soft" size="lg"> Активна </UBadge>
        </div>
      </template>

      <div class="flex items-center justify-between">
        <div>
          <h4 class="text-2xl font-bold text-default">
            {{ currentPlan.name }}
          </h4>
          <p class="text-muted">
            {{
              currentPlan.price === 0
                ? "Бесплатно"
                : `${formatPrice(currentPlan.price)}/мес`
            }}
          </p>
        </div>
        <UButton color="primary" variant="soft"> Изменить план </UButton>
      </div>

      <div class="mt-4 pt-4 border-t border-default">
        <p class="text-sm font-medium text-default mb-2">Включено:</p>
        <ul class="space-y-1">
          <li
            v-for="feature in currentPlan.features"
            :key="feature"
            class="flex items-center gap-2 text-sm text-muted"
          >
            <UIcon name="i-lucide-check" class="size-4 text-success" />
            {{ feature }}
          </li>
        </ul>
      </div>
    </UCard>

    <!-- Available Plans -->
    <div>
      <h3 class="text-lg font-semibold text-default mb-4">Доступные планы</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <UCard
          v-for="plan in plans"
          :key="plan.name"
          :class="[
            'relative',
            plan.popular ? 'ring-2 ring-primary' : '',
            plan.current ? 'bg-muted/30' : '',
          ]"
        >
          <UBadge
            v-if="plan.popular"
            color="primary"
            class="absolute -top-3 left-1/2 -translate-x-1/2"
          >
            Популярный
          </UBadge>

          <div class="text-center mb-4">
            <h4 class="text-lg font-semibold text-default">{{ plan.name }}</h4>
            <p class="text-sm text-muted">{{ plan.description }}</p>
          </div>

          <div class="text-center mb-4">
            <span class="text-3xl font-bold text-default">
              {{ plan.price === 0 ? "0" : formatPrice(plan.price) }}
            </span>
            <span class="text-muted">/мес</span>
          </div>

          <ul class="space-y-2 mb-6">
            <li
              v-for="feature in plan.features"
              :key="feature"
              class="flex items-start gap-2 text-sm"
            >
              <UIcon
                name="i-lucide-check"
                class="size-4 text-success shrink-0 mt-0.5"
              />
              <span class="text-muted">{{ feature }}</span>
            </li>
          </ul>

          <UButton
            :color="
              plan.current ? 'neutral' : plan.popular ? 'primary' : 'neutral'
            "
            :variant="plan.current ? 'outline' : 'solid'"
            :disabled="plan.current"
            block
          >
            {{ plan.current ? "Текущий план" : "Выбрать" }}
          </UButton>
        </UCard>
      </div>
    </div>

    <!-- Payment Methods -->
    <UCard>
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div
              class="size-10 rounded-lg bg-info/10 flex items-center justify-center"
            >
              <UIcon name="i-lucide-credit-card" class="size-5 text-info" />
            </div>
            <div>
              <h3 class="font-semibold text-default">Способы оплаты</h3>
              <p class="text-sm text-muted">Ваши сохранённые карты</p>
            </div>
          </div>
          <UButton color="primary" variant="ghost" icon="i-lucide-plus">
            Добавить карту
          </UButton>
        </div>
      </template>

      <div class="text-center py-8">
        <UIcon
          name="i-lucide-credit-card"
          class="size-12 text-muted mx-auto mb-3"
        />
        <p class="text-muted">Нет сохранённых способов оплаты</p>
        <p class="text-sm text-muted">
          Добавьте карту для автоматического продления подписки
        </p>
      </div>
    </UCard>

    <!-- Payment History -->
    <UCard>
      <template #header>
        <div class="flex items-center gap-3">
          <div
            class="size-10 rounded-lg bg-success/10 flex items-center justify-center"
          >
            <UIcon name="i-lucide-receipt" class="size-5 text-success" />
          </div>
          <div>
            <h3 class="font-semibold text-default">История платежей</h3>
            <p class="text-sm text-muted">Ваши предыдущие транзакции</p>
          </div>
        </div>
      </template>

      <div v-if="paymentHistory.length === 0" class="text-center py-8">
        <UIcon name="i-lucide-inbox" class="size-12 text-muted mx-auto mb-3" />
        <p class="text-muted">История платежей пуста</p>
      </div>

      <div v-else class="divide-y divide-default">
        <div
          v-for="payment in paymentHistory"
          :key="payment.id"
          class="flex items-center justify-between py-3"
        >
          <div>
            <p class="font-medium text-default">{{ payment.description }}</p>
            <p class="text-sm text-muted">{{ formatDate(payment.date) }}</p>
          </div>
          <div class="text-right">
            <p class="font-semibold text-default">
              {{ formatPrice(payment.amount) }}
            </p>
            <UBadge color="success" variant="soft" size="sm"> Оплачено </UBadge>
          </div>
        </div>
      </div>
    </UCard>
  </div>
</template>
