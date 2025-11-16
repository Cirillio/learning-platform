export default defineAppConfig({
  name: "UniversityClient",
  version: "1.0.0",
  ui: {
    colors: {
      primary: "lime",
      secondary: "cyan",
      neutral: "zinc",
    },
    button: {
      slots: {
        base: "cursor-pointer !transition-all !duration-200 !ease-in-out",
      },
      variants: {
        variant: {
          outline: "bg-transparent hover:bg-inverted border-muted ",
        },
      },
    },
    card: {
      slots: {
        root: "!dark:bg-muted/50 !bg-elevated/50 !ring-0",
        header: "border-0",
      },
    },
    input: {
      slots: {
        base: "!transition-all !duration-200 !ease-in-out !bg-default rounded-sm !py-3.5 !px-6",
      },
    },
  },
});
