export default defineAppConfig({
  name: "UniversityClient",
  version: "1.0.0",
  ui: {
    colors: {
      primary: "lime",
      secondary: "rose",
      neutral: "zinc",
    },
    main: {
      base: "dark:!bg-elevated/25 !bg-muted/50",
    },
    card: {
      slots: {
        root: "!dark:bg-muted/50 !bg-elevated/50 !ring-0",
        header: "border-0",
      },
    },
  },
});
