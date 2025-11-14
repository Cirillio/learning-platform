/**
 * Composable для валидации форм с использованием Zod схем
 *
 * Пример использования:
 *
 * ```typescript
 * import { loginSchema, type LoginForm } from "~/schemas/auth.schema";
 *
 * const {
 *   data,        // reactive данные формы
 *   errors,      // reactive объект с ошибками по полям
 *   isValid,     // computed: true если нет ошибок
 *   isDirty,     // true если форма была изменена
 *   isValidating,// true во время валидации
 *   handleSubmit,// функция для обработки отправки формы
 *   handleChange,// функция для обработки изменения поля
 *   handleBlur,  // функция для обработки потери фокуса
 *   validateAll, // валидировать все поля
 *   validateField,// валидировать конкретное поле
 *   setValue,    // установить значение поля
 *   getValue,    // получить значение поля
 *   setError,    // установить ошибку для поля
 *   clearErrors, // очистить ошибки
 *   reset,       // сбросить форму
 * } = useFormValidation<LoginForm>({
 *   schema: loginSchema,
 *   initialData: { username: "", password: "" },
 *   validateOnChange: true,  // валидировать при изменении
 *   validateOnBlur: true,    // валидировать при потере фокуса
 *   validateOnSubmit: true,  // валидировать при отправке
 * });
 *
 * // Использование в шаблоне:
 * <input
 *   v-model="data.username"
 *   @blur="handleBlur('username')"
 *   @input="handleChange('username', $event.target.value)"
 * />
 * <span v-if="errors.username">{{ errors.username }}</span>
 *
 * // Отправка формы:
 * const onSubmit = async () => {
 *   await handleSubmit(async (formData) => {
 *     // отправить данные на сервер
 *     await api.login(formData);
 *   });
 * };
 * ```
 */
