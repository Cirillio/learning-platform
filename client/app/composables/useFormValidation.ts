import type { ZodSchema, ZodError } from "zod";

export interface FormValidationState<T = any> {
  data: T;
  errors: Record<string, string>;
  isValid: boolean;
  isDirty: boolean;
  isValidating: boolean;
}

export interface UseFormValidationOptions<T = any> {
  schema?: ZodSchema<T>;
  initialData?: Partial<T>;
  validateOnChange?: boolean;
  validateOnBlur?: boolean;
  validateOnSubmit?: boolean;
}

export function useFormValidation<T extends Record<string, any> = any>(
  options: UseFormValidationOptions<T> = {}
) {
  const {
    schema,
    initialData = {} as Partial<T>,
    validateOnChange = true,
    validateOnBlur = false,
    validateOnSubmit = true,
  } = options;

  // Reactive state
  const data = reactive<T>({ ...initialData } as T);
  const errors = ref<Record<string, string>>({});
  const isValidating = ref(false);
  const isDirty = ref(false);

  // Computed properties
  const isValid = computed(() => Object.keys(errors.value).length === 0);

  // Validation function
  const validate = async (field?: keyof T): Promise<boolean> => {
    if (!schema) return true;

    isValidating.value = true;

    try {
      if (field) {
        // Validate single field
        const fieldSchema = (schema as any).shape?.[field];
        if (fieldSchema) {
          const result = await fieldSchema.safeParseAsync((data as any)[field]);
          if (!result.success) {
            const fieldErrors = result.error.issues;
            errors.value[field as string] =
              fieldErrors[0]?.message || "Invalid value";
          } else {
            delete errors.value[field as string];
          }
        }
      } else {
        // Validate all fields
        const result = await schema.safeParseAsync(toRaw(data));

        if (!result.success) {
          const newErrors: Record<string, string> = {};

          result.error.issues.forEach((issue) => {
            const field = issue.path[0] as string;
            if (!newErrors[field]) {
              newErrors[field] = issue.message;
            }
          });

          errors.value = newErrors;
        } else {
          errors.value = {};
        }
      }

      return Object.keys(errors.value).length === 0;
    } catch (error) {
      console.error("Validation error:", error);
      return false;
    } finally {
      isValidating.value = false;
    }
  };

  // Validate single field
  const validateField = async (field: keyof T): Promise<boolean> => {
    return validate(field);
  };

  // Validate all fields
  const validateAll = async (): Promise<boolean> => {
    return validate();
  };

  // Clear errors
  const clearErrors = (field?: keyof T): void => {
    if (field) {
      delete errors.value[field as string];
    } else {
      errors.value = {};
    }
  };

  // Set error for field
  const setError = (field: keyof T, message: string): void => {
    errors.value[field as string] = message;
  };

  // Reset form
  const reset = (newData?: Partial<T>): void => {
    Object.assign(data, { ...initialData, ...newData } as T);
    errors.value = {};
    isDirty.value = false;
  };

  // Set field value
  const setValue = <K extends keyof T>(field: K, value: T[K]): void => {
    (data as any)[field] = value;
    isDirty.value = true;

    if (validateOnChange) {
      validateField(field);
    }
  };

  // Get field value
  const getValue = <K extends keyof T>(field: K): T[K] => {
    return (data as any)[field];
  };

  // Handle field change
  const handleChange = <K extends keyof T>(field: K, value: T[K]): void => {
    setValue(field, value);
  };

  // Handle field blur
  const handleBlur = <K extends keyof T>(field: K): void => {
    if (validateOnBlur) {
      validateField(field);
    }
  };

  // Submit handler
  const handleSubmit = async (
    callback?: (data: T) => void | Promise<void>
  ): Promise<boolean> => {
    const valid = validateOnSubmit ? await validateAll() : true;

    if (valid && callback) {
      await callback(toRaw(data) as T);
    }

    return valid;
  };

  // Watch for data changes to mark as dirty
  watch(
    data,
    () => {
      isDirty.value = true;
    },
    { deep: true }
  );

  return {
    // State
    data: readonly(data),
    errors: readonly(errors),
    isValid,
    isDirty: readonly(isDirty),
    isValidating: readonly(isValidating),

    // Methods
    validate,
    validateField,
    validateAll,
    clearErrors,
    setError,
    reset,
    setValue,
    getValue,
    handleChange,
    handleBlur,
    handleSubmit,
  };
}
