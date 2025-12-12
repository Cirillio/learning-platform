export default defineAppConfig({
  ui: {
    // Монохромная корпоративная палитра
    colors: {
      primary: "teal",
      secondary: "indigo",
      neutral: "neutral",
      success: "emerald",
      error: "red",
    },

    // Крупная корпоративная типографика
    typography: {
      h1: "text-4xl md:text-6xl font-bold leading-tight tracking-tight",
      h2: "text-3xl md:text-5xl font-bold leading-tight",
      h3: "text-2xl md:text-4xl font-bold leading-tight",
      p: "text-lg leading-relaxed",
      strong: "font-bold",
    },

    button: {
      slots: {
        base: "cursor-pointer transition duration-150 ease-in-out",
      },
    },

    select: {
      slots: {
        base: "!cursor-pointer transition duration-150 ease-in-out shadow-xs",
        item: "cursor-pointer hover:bg-primary/10 transition duration-150 ease-in-out",
        label: "!text-primary",
        value: "font-semibold",
        content: "!bg-default/90 !backdrop-blur-sm shadow-md",
      },
    },

    input: {
      slots: {
        base: "transition duration-150 ease-in-out",
      },
    },
    card: {
      slots: {
        root: "shadow-xs dark:bg-muted/25! bg-muted/75!",
        body: "p-3!",
      },
    },
  },
});
