import type { ButtonProps } from "@nuxt/ui";

export const getHeaderMenuItems = (config: { onLogout: () => void }) => {
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
