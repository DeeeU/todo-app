<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
      <h1 class="text-2xl font-bold text-gray-800 mb-4">
        🎉 Todo App - Frontend Ready!
      </h1>

      <div class="space-y-2">
        <div class="flex items-center space-x-2">
          <input
            type="checkbox"
            class="w-4 h-4 text-blue-600"
            checked
          >
          <span class="text-gray-700 line-through">Django REST API 完成</span>
        </div>

        <div class="flex items-center space-x-2">
          <input
            type="checkbox"
            class="w-4 h-4 text-blue-600"
            checked
          >
          <span class="text-gray-700 line-through">Nuxt.js 環境構築</span>
        </div>

        <div class="flex items-center space-x-2">
          <input
            type="checkbox"
            class="w-4 h-4 text-blue-600"
            checked
          >
          <span class="text-gray-700 line-through">Tailwind CSS 導入</span>
        </div>

        <div class="flex items-center space-x-2">
          <input
            type="checkbox"
            class="w-4 h-4 text-blue-600"
          >
          <span class="text-gray-700">Todo画面作成 ← Next!</span>
        </div>
      </div>

      <div class="mt-6 p-4 bg-blue-50 rounded-lg">
        <p class="text-sm text-blue-700">
          💡 Tailwind CSS が正常に動作しています！
        </p>
      </div>
    </div>
  </div>
</template>
