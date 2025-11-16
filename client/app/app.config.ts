export default defineAppConfig({
  name: "UniversityClient",
  version: "1.0.0",
  ui: {
    colors: {
      neutral: "zinc",
    },
    button: {
      slots: {
        base: "cursor-pointer rounded-sm !transition-all !duration-200 !ease-in-out",
      },
      variants: {
        variant: {
          outline: "bg-transparent hover:bg-inverted border-muted ",
        },
      },
    },
    card: {
      slots: {
        root: "!bg-transparent !p-1  !ring-primary rounded-xs backdrop-blur-sm hover:!ring-secondary/50 transition-all duration-200 ease-in-out",
        header: "border-0",
        body: "!px-3 !py-2 bg-muted h-full rounded-xs",
      },
    },
    input: {
      slots: {
        base: "!transition-all !duration-200 !ease-in-out !bg-default rounded-xs !py-3.5 !px-6",
      },
    },
  },
});
