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
        root: "group",
        base: "!transition-all hover:!ring-secondary !text-base !duration-200 !ease-in-out !bg-default rounded-xs !py-3.5 !px-6",
        leadingIcon:
          "group-hover:!bg-primary  transition-all duration-150 ease-in-out",
      },
    },
    selectMenu: {
      slots: {
        trailing:
          "ring ring-primary bg-default group-hover:bg-primary  transition-all duration-150 ease-in-out size-fit right-4 top-1/2 -translate-y-1/2 rounded-xs !p-0 grid place-center",
        trailingIcon:
          "group-hover:!bg-default bg-primary  transition-all duration-150 ease-in-out",
        empty: "!text-primary/50",
        placeholder: "!text-primary/75",
        input: "group-hover:!border-secondary *:!text-lg",
        content:
          "hover:ring-secondary !transition-all !duration-150 !ease-in-out !rounded-xs",
        item: "!text-lg cursor-pointer rounded-xs hover:bg-primary hover:!text-inverted !transition-all !duration-150 !ease-in-out",
        base: "!rounded-xs !text-secondary hover:ring-secondary/70 cursor-pointer !text-base !py-3.5 !px-4 !transition-all !duration-200 !ease-in-out ",
      },
    },
    modal: {
      variants: {
        fullscreen: {
          false: {
            close:
              "bg-accent/15 hover:bg-accent/25 text-accent ring ring-accent rounded-xs *:size-8 p-0 relative top-0 left-0",
            header: "text-4xl font-bold border-primary justify-between",
            content: "rounded-sm ring-primary p-0",
          },
        },
      },
    },
  },
});
