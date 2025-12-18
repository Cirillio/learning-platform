import type { ButtonProps } from "@nuxt/ui";

export const getHeaderMenuItems = (config: {
  onLogout: () => void;
  onFeedback: () => void;
}) => {
  const headerMenuItems = ref<ButtonProps[]>([
    {
      label: "Настройки",
      icon: "heroicons:cog-6-tooth",
      href: "/settings",
      color: "neutral",
      variant: "subtle",
      size: "md",
    },
    {
      label: "Обратная связь",
      icon: "heroicons:chat-bubble-left-right",
      color: "neutral",
      variant: "subtle",
      size: "md",
      onClick: config.onFeedback,
    },
    {
      label: "Выйти",
      icon: "heroicons:arrow-uturn-right",
      color: "error",
      size: "md",
      variant: "subtle",
      onClick: config.onLogout,
    },
  ]);

  return { headerMenuItems };
};
