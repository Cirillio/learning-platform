# План переноса на Android через Capacitor

## Обзор

Этот документ описывает пошаговый план переноса учебного портала на Android с использованием Capacitor.

**Время выполнения:**
- Минимальная версия (рабочее приложение): **2-3 часа**
- Полная версия (полированное приложение): **5-8 часов**

---

## Этап 1: Подготовка (10-15 минут)

### 1.1 Установка Capacitor

```bash
cd client
npm install @capacitor/core @capacitor/cli
npm install @capacitor/android
```

### 1.2 Инициализация проекта

```bash
npx cap init
# App name: University Portal
# App ID: com.university.portal
```

### 1.3 Обновить nuxt.config.ts

```typescript
export default defineNuxtConfig({
  ssr: false, // ВАЖНО: Capacitor работает только с SPA

  app: {
    baseURL: './', // Для корректных путей в мобильном приложении
  },

  // Остальная конфигурация...
})
```

---

## Этап 2: Базовая сборка (30-40 минут)

### 2.1 Сборка Nuxt приложения

```bash
npm run build
```

### 2.2 Добавление Android платформы

```bash
npx cap add android
```

Эта команда создаст папку `android/` с проектом Android Studio.

### 2.3 Копирование билда в нативное приложение

```bash
npx cap sync
```

Эта команда:
- Копирует собранное приложение из `.output/public` в `android/app/src/main/assets/public`
- Обновляет плагины

### 2.4 Открытие в Android Studio

```bash
npx cap open android
```

Установи Android Studio, если ещё не установлена:
https://developer.android.com/studio

### 2.5 Запуск на эмуляторе или устройстве

1. Создай эмулятор в Android Studio (AVD Manager)
2. Нажми "Run" (зелёный треугольник)
3. Приложение запустится на эмуляторе

**Поздравляю! Базовое приложение работает! 🎉**

---

## Этап 3: Адаптация хранилища (30 минут)

### 3.1 Установка плагина для хранилища

```bash
npm install @capacitor/preferences
```

### 3.2 Создать универсальный composable для хранения

```typescript
// client/composables/useStorage.ts

import { Preferences } from '@capacitor/preferences'

export const useStorage = () => {
  /**
   * Сохранить значение
   * Работает и на вебе, и на мобилке
   */
  const setItem = async (key: string, value: string) => {
    try {
      await Preferences.set({ key, value })
    } catch (error) {
      console.error('Storage error:', error)
    }
  }

  /**
   * Получить значение
   */
  const getItem = async (key: string): Promise<string | null> => {
    try {
      const { value } = await Preferences.get({ key })
      return value
    } catch (error) {
      console.error('Storage error:', error)
      return null
    }
  }

  /**
   * Удалить значение
   */
  const removeItem = async (key: string) => {
    try {
      await Preferences.remove({ key })
    } catch (error) {
      console.error('Storage error:', error)
    }
  }

  /**
   * Очистить всё хранилище
   */
  const clear = async () => {
    try {
      await Preferences.clear()
    } catch (error) {
      console.error('Storage error:', error)
    }
  }

  return {
    setItem,
    getItem,
    removeItem,
    clear
  }
}
```

### 3.3 Обновить auth store

```typescript
// client/stores/auth.ts

import { defineStore } from 'pinia'
import { useStorage } from '~/composables/useStorage'

export const useAuthStore = defineStore('auth', () => {
  const { setItem, getItem, removeItem } = useStorage()

  const token = ref<string | null>(null)
  const user = ref<any>(null)

  // Загрузить токен при инициализации
  const loadToken = async () => {
    token.value = await getItem('auth_token')
  }

  // Сохранить токен
  const setToken = async (newToken: string) => {
    token.value = newToken
    await setItem('auth_token', newToken)
  }

  // Выход
  const logout = async () => {
    token.value = null
    user.value = null
    await removeItem('auth_token')
  }

  return {
    token,
    user,
    loadToken,
    setToken,
    logout
  }
})
```

### 3.4 Инициализация при запуске

```typescript
// client/app.vue

<script setup lang="ts">
const authStore = useAuthStore()

// Загрузить токен при запуске
onMounted(async () => {
  await authStore.loadToken()
})
</script>
```

---

## Этап 4: Настройка иконки и Splash Screen (30 минут)

### 4.1 Подготовить ресурсы

Создай следующие файлы:
- `client/public/icon.png` - 1024x1024px (иконка приложения)
- `client/public/splash.png` - 2732x2732px (экран загрузки)

### 4.2 Установить плагин для генерации ресурсов

```bash
npm install -g cordova-res
```

### 4.3 Сгенерировать иконки и splash screens

```bash
cordova-res android --skip-config --copy
```

### 4.4 Настроить Splash Screen

```bash
npm install @capacitor/splash-screen
```

```typescript
// client/app.vue

import { SplashScreen } from '@capacitor/splash-screen'

onMounted(async () => {
  // Скрыть splash screen после загрузки
  await authStore.loadToken()
  await SplashScreen.hide()
})
```

---

## Этап 5: Push-уведомления (1-2 часа, опционально)

### 5.1 Установка плагина

```bash
npm install @capacitor/push-notifications
```

### 5.2 Настройка Firebase Cloud Messaging

1. Создай проект в Firebase Console: https://console.firebase.google.com
2. Добавь Android приложение (package name: `com.university.portal`)
3. Скачай `google-services.json`
4. Помести в `android/app/google-services.json`

### 5.3 Обновить android/build.gradle

```gradle
buildscript {
    dependencies {
        classpath 'com.google.gms:google-services:4.3.15'
    }
}
```

### 5.4 Обновить android/app/build.gradle

```gradle
apply plugin: 'com.google.gms.google-services'
```

### 5.5 Создать composable для push-уведомлений

```typescript
// client/composables/usePushNotifications.ts

import { PushNotifications } from '@capacitor/push-notifications'

export const usePushNotifications = () => {
  const registerPush = async () => {
    // Запрос разрешений
    const result = await PushNotifications.requestPermissions()

    if (result.receive === 'granted') {
      // Регистрация
      await PushNotifications.register()
    }
  }

  // Получение токена устройства
  PushNotifications.addListener('registration', (token) => {
    console.log('Push token:', token.value)
    // Отправить токен на бэкенд
    sendTokenToBackend(token.value)
  })

  // Получение уведомления
  PushNotifications.addListener('pushNotificationReceived', (notification) => {
    console.log('Notification received:', notification)
  })

  // Клик по уведомлению
  PushNotifications.addListener('pushNotificationActionPerformed', (action) => {
    console.log('Notification action:', action)
    // Навигация к нужной странице
  })

  const sendTokenToBackend = async (token: string) => {
    const api = useApi()
    await api.post('/api/notifications/register-device/', { token })
  }

  return {
    registerPush
  }
}
```

### 5.6 Использование

```typescript
// client/app.vue

const { registerPush } = usePushNotifications()

onMounted(async () => {
  await authStore.loadToken()

  if (authStore.isAuthenticated) {
    await registerPush()
  }
})
```

---

## Этап 6: Работа с камерой (1 час, опционально)

### 6.1 Установка плагина

```bash
npm install @capacitor/camera
```

### 6.2 Создать composable для камеры

```typescript
// client/composables/useCamera.ts

import { Camera, CameraResultType, CameraSource } from '@capacitor/camera'

export const useCamera = () => {
  /**
   * Выбрать изображение из камеры или галереи
   */
  const pickImage = async () => {
    try {
      const image = await Camera.getPhoto({
        quality: 90,
        allowEditing: true,
        resultType: CameraResultType.Uri,
        source: CameraSource.Prompt, // Показать выбор: камера или галерея
      })

      return image.webPath
    } catch (error) {
      console.error('Camera error:', error)
      return null
    }
  }

  /**
   * Сделать фото с камеры
   */
  const takePhoto = async () => {
    try {
      const image = await Camera.getPhoto({
        quality: 90,
        allowEditing: false,
        resultType: CameraResultType.Uri,
        source: CameraSource.Camera,
      })

      return image.webPath
    } catch (error) {
      console.error('Camera error:', error)
      return null
    }
  }

  return {
    pickImage,
    takePhoto
  }
}
```

### 6.3 Использование в компоненте

```vue
<!-- client/components/forms/ProfileEditForm.vue -->

<script setup lang="ts">
const { pickImage } = useCamera()

const handleAvatarUpload = async () => {
  const imagePath = await pickImage()

  if (imagePath) {
    // Загрузить на сервер
    await uploadAvatar(imagePath)
  }
}
</script>

<template>
  <div>
    <button @click="handleAvatarUpload">
      Выбрать фото
    </button>
  </div>
</template>
```

### 6.4 Настроить permissions в AndroidManifest.xml

```xml
<!-- android/app/src/main/AndroidManifest.xml -->

<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
```

---

## Этап 7: Адаптивный UI для мобильных (2 часа)

### 7.1 Мобильная навигация (Bottom Tabs)

```vue
<!-- client/components/layout/BottomNavigation.vue -->

<template>
  <nav class="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
    <div class="flex justify-around items-center h-16">
      <NuxtLink to="/dashboard" class="flex flex-col items-center">
        <Icon name="heroicons:home" class="w-6 h-6" />
        <span class="text-xs mt-1">Главная</span>
      </NuxtLink>

      <NuxtLink to="/courses" class="flex flex-col items-center">
        <Icon name="heroicons:book-open" class="w-6 h-6" />
        <span class="text-xs mt-1">Курсы</span>
      </NuxtLink>

      <NuxtLink to="/notifications" class="flex flex-col items-center">
        <Icon name="heroicons:bell" class="w-6 h-6" />
        <span class="text-xs mt-1">Уведомления</span>
      </NuxtLink>

      <NuxtLink to="/profile" class="flex flex-col items-center">
        <Icon name="heroicons:user" class="w-6 h-6" />
        <span class="text-xs mt-1">Профиль</span>
      </NuxtLink>
    </div>
  </nav>
</template>
```

### 7.2 Адаптивный layout

```vue
<!-- client/layouts/default.vue -->

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Desktop: Sidebar -->
    <aside class="hidden md:block fixed left-0 top-0 h-screen w-64 bg-white border-r">
      <SidebarNavigation />
    </aside>

    <!-- Main content -->
    <main class="md:ml-64 pb-16 md:pb-0">
      <slot />
    </main>

    <!-- Mobile: Bottom navigation -->
    <BottomNavigation />
  </div>
</template>
```

### 7.3 Touch-friendly кнопки

```vue
<!-- Минимальный размер для мобильных: 44x44px -->

<UButton
  size="lg"
  class="min-h-[44px] min-w-[44px]"
>
  Нажми меня
</UButton>
```

### 7.4 Безопасные зоны (Safe Area)

```typescript
// nuxt.config.ts

export default defineNuxtConfig({
  app: {
    head: {
      meta: [
        {
          name: 'viewport',
          content: 'width=device-width, initial-scale=1, viewport-fit=cover'
        }
      ]
    }
  }
})
```

```css
/* client/assets/css/main.css */

body {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```

---

## Этап 8: Проверка состояния сети (30 минут, опционально)

### 8.1 Установка плагина

```bash
npm install @capacitor/network
```

### 8.2 Создать composable

```typescript
// client/composables/useNetwork.ts

import { Network } from '@capacitor/network'

export const useNetwork = () => {
  const isOnline = ref(true)

  const checkStatus = async () => {
    const status = await Network.getStatus()
    isOnline.value = status.connected
  }

  // Слушать изменения
  Network.addListener('networkStatusChange', (status) => {
    isOnline.value = status.connected

    if (!status.connected) {
      // Показать уведомление
      console.warn('Нет подключения к интернету')
    }
  })

  return {
    isOnline,
    checkStatus
  }
}
```

### 8.3 Использование

```vue
<script setup lang="ts">
const { isOnline } = useNetwork()
</script>

<template>
  <div v-if="!isOnline" class="bg-red-500 text-white p-4 text-center">
    Нет подключения к интернету
  </div>
</template>
```

---

## Этап 9: Сборка production APK (30 минут)

### 9.1 Обновить версию приложения

```json
// capacitor.config.json

{
  "appId": "com.university.portal",
  "appName": "University Portal",
  "version": "1.0.0"
}
```

### 9.2 Сборка Nuxt

```bash
npm run build
npx cap sync
```

### 9.3 Сборка APK в Android Studio

1. Открой проект: `npx cap open android`
2. Build → Generate Signed Bundle / APK
3. Выбери APK
4. Создай keystore (первый раз)
5. Build

APK будет в `android/app/build/outputs/apk/release/`

### 9.4 Альтернатива: через Gradle

```bash
cd android
./gradlew assembleRelease
```

---

## Этап 10: Тестирование (1-2 часа)

### Чек-лист тестирования:

- [ ] Регистрация и авторизация
- [ ] Сохранение токена (остаёшься залогиненным после перезапуска)
- [ ] Просмотр курсов
- [ ] Отправка заданий
- [ ] Загрузка файлов
- [ ] Комментарии
- [ ] Уведомления (push)
- [ ] Работа без интернета (базовая)
- [ ] Навигация (все страницы)
- [ ] Ротация экрана
- [ ] Клавиатура (не перекрывает поля ввода)
- [ ] Кнопка назад (Android back button)

---

## Дополнительные плагины (опционально)

### Haptic Feedback (вибрация)

```bash
npm install @capacitor/haptics
```

```typescript
import { Haptics, ImpactStyle } from '@capacitor/haptics'

// При клике на кнопку
await Haptics.impact({ style: ImpactStyle.Medium })
```

### App Launcher (открытие других приложений)

```bash
npm install @capacitor/app-launcher
```

### Status Bar (цвет статус-бара)

```bash
npm install @capacitor/status-bar
```

```typescript
import { StatusBar, Style } from '@capacitor/status-bar'

// Тёмная тема
await StatusBar.setStyle({ style: Style.Dark })
```

---

## Capacitor конфигурация

### capacitor.config.ts

```typescript
import { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'com.university.portal',
  appName: 'University Portal',
  webDir: '.output/public',
  server: {
    androidScheme: 'https',
    // Для разработки (подключение к локальному серверу)
    // url: 'http://192.168.1.100:3000',
    // cleartext: true
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: '#4f46e5',
      showSpinner: true,
      spinnerColor: '#ffffff'
    },
    PushNotifications: {
      presentationOptions: ['badge', 'sound', 'alert']
    }
  }
}

export default config
```

---

## Отладка

### Chrome DevTools для мобильного приложения

1. Подключи устройство по USB
2. Включи USB debugging на Android
3. Открой Chrome: `chrome://inspect`
4. Выбери своё приложение
5. Inspect

### Логи через Android Studio

```bash
npx cap open android
# Внизу: Logcat
# Фильтр: Capacitor
```

---

## Полезные команды

```bash
# Пересобрать и синхронизировать
npm run build && npx cap sync

# Открыть Android Studio
npx cap open android

# Обновить плагины
npx cap update

# Посмотреть установленные плагины
npx cap ls

# Добавить iOS (если понадобится в будущем)
npx cap add ios
```

---

## Частые проблемы и решения

### Проблема: Белый экран после запуска

**Решение:**
1. Убедись что `ssr: false` в `nuxt.config.ts`
2. Проверь что `baseURL: './'`
3. Пересобери: `npm run build && npx cap sync`

### Проблема: CORS ошибки

**Решение:**
Добавь в Django settings:
```python
CORS_ALLOWED_ORIGINS = [
    'capacitor://localhost',
    'https://localhost'
]
```

### Проблема: Клавиатура перекрывает поля ввода

**Решение:**
```bash
npm install @capacitor/keyboard
```

```typescript
import { Keyboard } from '@capacitor/keyboard'

Keyboard.addListener('keyboardWillShow', () => {
  // Сдвинуть контент вверх
})
```

---

## Timeline (оценка времени)

| Этап | Минимальная версия | Полная версия |
|------|-------------------|---------------|
| 1. Подготовка | 15 мин | 15 мин |
| 2. Базовая сборка | 40 мин | 40 мин |
| 3. Хранилище | 30 мин | 30 мин |
| 4. Иконки/Splash | - | 30 мин |
| 5. Push уведомления | - | 2 часа |
| 6. Камера | - | 1 час |
| 7. Адаптивный UI | 30 мин | 2 часа |
| 8. Проверка сети | - | 30 мин |
| 9. Production сборка | 30 мин | 30 мин |
| 10. Тестирование | 30 мин | 2 часа |
| **Итого** | **~3 часа** | **~9 часов** |

---

## Ресурсы

- Capacitor документация: https://capacitorjs.com/docs
- Capacitor плагины: https://capacitorjs.com/docs/plugins
- Android Studio: https://developer.android.com/studio
- Firebase Console: https://console.firebase.google.com
- Nuxt Capacitor пример: https://github.com/nuxt-community/capacitor-module

---

## Заключение

Перенос Nuxt приложения на Android через Capacitor - это относительно простой процесс, который не требует переписывания всего кода. Основная работа заключается в:

1. Настройке билда (30 мин)
2. Адаптации хранилища (30 мин)
3. Тестировании и доработке UI (1-2 часа)

Всё остальное - опциональные улучшения, которые можно добавлять постепенно.

**Главное:** делай код изначально универсальным (используй composables, избегай прямого обращения к `localStorage`), и перенос пройдёт максимально гладко!
