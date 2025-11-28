// composables/useCssVar.ts
export function useCssVar(
  elementRef: Ref<HTMLElement | null>,
  varName: string,
  getValue: (el: HTMLElement) => string | number
) {
  const isDev = process.env.NODE_ENV === "development";

  const setCssVar = (value: string | number) => {
    if (!elementRef.value) {
      if (isDev) console.warn(`[useCssVar] Element ref is null for ${varName}`);
      return;
    }

    const stringValue = typeof value === "number" ? `${value}px` : value;
    // Устанавливаем переменную глобально на :root
    document.documentElement.style.setProperty(varName, stringValue);

    if (isDev) {
      console.log(`[useCssVar] Set ${varName} = ${stringValue} globally`, {
        element: elementRef.value.tagName,
        class: elementRef.value.className,
        computedStyle: getComputedStyle(
          document.documentElement
        ).getPropertyValue(varName),
      });
    }
  };

  onMounted(() => {
    if (isDev) console.log(`[useCssVar] Mounted for ${varName}`);

    if (!elementRef.value) {
      if (isDev)
        console.error(
          `[useCssVar] Element ref is null on mount for ${varName}`
        );
      return;
    }

    const observer = new ResizeObserver(() => {
      if (elementRef.value) {
        const value = getValue(elementRef.value);
        if (isDev)
          console.log(
            `[useCssVar] ResizeObserver triggered for ${varName}`,
            value
          );
        setCssVar(value);
      }
    });

    observer.observe(elementRef.value);
    if (isDev)
      console.log(`[useCssVar] ResizeObserver attached for ${varName}`);

    // Первоначальная установка
    const value = getValue(elementRef.value);
    if (isDev) console.log(`[useCssVar] Initial value for ${varName}:`, value);
    setCssVar(value);

    onUnmounted(() => {
      if (isDev)
        console.log(
          `[useCssVar] Unmounted, disconnecting observer for ${varName}`
        );
      observer.disconnect();
    });
  });

  return {
    setCssVar,
  };
}

// Хелпер для высоты
export function useElementHeight(
  elementRef: Ref<HTMLElement | null>,
  varName: string = "--element-height"
) {
  const isDev = process.env.NODE_ENV === "development";
  if (isDev)
    console.log(`[useElementHeight] Initialized with varName: ${varName}`);

  return useCssVar(elementRef, varName, (el) => {
    const height = el.offsetHeight;
    if (isDev)
      console.log(
        `[useElementHeight] Calculated height for ${varName}:`,
        height
      );
    return height;
  });
}

// Хелпер для ширины
export function useElementWidth(
  elementRef: Ref<HTMLElement | null>,
  varName: string = "--element-width"
) {
  const isDev = process.env.NODE_ENV === "development";
  if (isDev)
    console.log(`[useElementWidth] Initialized with varName: ${varName}`);

  return useCssVar(elementRef, varName, (el) => {
    const width = el.offsetWidth;
    if (isDev)
      console.log(`[useElementWidth] Calculated width for ${varName}:`, width);
    return width;
  });
}
