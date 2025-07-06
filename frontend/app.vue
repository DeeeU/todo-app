<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
    <div class="max-w-md mx-auto">
      <!-- ヘッダー -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">
          📝 My Todo App
        </h1>
        <p class="text-gray-600">Django + Nuxt.js で作ったアプリ</p>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <!-- 成功メッセージ -->
        <div
          v-if="successMessage"
          class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded-md"
          >
          {{  successMessage }}
        </div>
        <h2 class="text-lg font-semibold text-gray-700 mb-4">新しいTodoを追加</h2>

        <form @submit.prevent="addTodo" class="space-y-3">
          <input
            v-model="newTodo.title"
            type="text"
            placeholder="タイトルを入力..."
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
            @keydown.enter.prevent="focusDescription"
          >
          <textarea
            ref="descriptionInput"
            v-model="newTodo.description"
            placeholder="説明（任意）"
            rows="2"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            @keydown.ctrl.enter="addTodo"
          ></textarea>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white py-2 px-4 rounded-md transition-colors"
          >
            {{ loading ? '追加中...' : '+ Todoを追加' }}
          </button>
        </form>
      </div>

      <div class="bg-white rounded-lg shadow-md p-4 mb-6">
        <div class="reactive">
          <input
            v-model="searchQuery"
            @input="debouncedSearch"
            type="text"
            placeholder="🔍 Todoを検索..."
            class="w-full px-4 py-2 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
          <div class="absolute left-3 top-2.5 text-gray-400">
            🔍
          </div>

          <div v-if="isSearching" class="absolute right-3 top-2.5">
            <div class="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full"></div>
          </div>
        </div>

        <div v-if="searchQuery" class="mt-2 text-sm text-gray-500">
          "{{ searchQuery }}"の検索結果: {{ todos.length }}件
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md">
        <!-- ヘッダー -->
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <h2 class="text-lg font-semibold text-gray-700">
              Todoリスト ({{ todos.length }}個)
            </h2>
            <button
              @click="refreshTodos"
              class="text-blue-500 hover:text-blue-600 transition-colors"
            >
              🔄 更新
            </button>
          </div>
        </div>

        <div class="p-6">
          <div v-if="loading" class="text-center py-8">
            <p class="text-gray-500">読み込み中...</p>
          </div>

          <div v-else-if="todos.length === 0" class="text-center py-8">
            <p class="text-gray-500 mb-2">まだTodoがありません</p>
            <p class="text-sm text-gray-400">上のフォームから追加してみましょう！</p>
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="todo in todos"
              :key="todo.id"
              class="flex items-center space-x-3 p-3 border border-gray-200 rounded-md hover:bg-gray-50 transition-colors"
            >
              <!-- チェックボックス -->
              <input
                :id="`todo-${todo.id}`"
                type="checkbox"
                :checked="todo.completed"
                @change="toggleTodo(todo)"
                class="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
              >

              <div class="flex-1">
                <label
                  :for="`todo-${todo.id}`"
                  :class="[
                    'block font-medium cursor-pointer',
                    todo.completed
                      ? 'text-gray-500 line-through'
                      : 'text-gray-800'
                  ]"
                >
                  {{ todo.title }}
                </label>

                <p
                  v-if="todo.description"
                  :class="[
                    'text-sm mt-1',
                    todo.completed
                      ? 'text-gray-400 line-through'
                      : 'text-gray-600'
                  ]"
                >
                  {{ todo.description }}
                </p>

                <p class="text-xs text-gray-400 mt-1">
                  {{ formatDate(todo.created_at) }}
                </p>
              </div>

              <!-- 削除ボタン -->
              <button
                @click="removeTodo(todo.id)"
                class="text-red-500 hover:text-red-600 p-1 transition-colors"
                title="削除"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="todos.length > 0" class="mt-6 bg-white rounded-lg shadow-md p-4">
        <div class="flex justify-between text-sm">
          <span class="text-gray-600">
            完了: {{ completedCount }}個
          </span>
          <span class="text-gray-600">
            残り: {{ remainingCount }}個
          </span>
        </div>

        <div class="mt-2 bg-gray-200 rounded-full h-2">
          <div
            class="bg-blue-500 h-2 rounded-full transition-all duration-300"
            :style="{ width: `${progressPercentage}%` }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// API通信用のcomposableを使用
const { fetchTodos, createTodo, updateTodo, deleteTodo } = useTodos()

// リアクティブデータ
const searchQuery = ref('')
const isSearching = ref(false)
const descriptionInput = ref()
const successMessage = ref('')
const todos = ref<Todo[]>([])
const loading = ref(true)
const newTodo = reactive({
  title: '',
  description: ''
})

// バウンス用のタイマー
let searchTimeout: NodeJS.Timeout | null = null

const debouncedSearch = () => {
  isSearching.value = true

  // 前回のタイマーをクリア
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }

  // 500ms後に検索実行
  searchTimeout = setTimeout(async () => {
    await refreshTodos()
    isSearching.value = false
  }, 500)
}

// Todoリスト取得を検索対応に修正
const refreshTodos = async () => {
  console.log('refreshTodos 開始')
  loading.value = true
  try {
    // 検索クエリがあれば検索APIを使用
    const { fetchTodos } = useTodos()
    const searchParams = searchQuery.value.trim()
      ? { search: searchQuery.value.trim() }
      : {}

    todos.value = await fetchTodos(searchParams)
    console.log('Todo取得完了:', todos.value.length, '件')
  } catch (error) {
    console.error('リフレッシュエラー:', error)
  } finally {
    loading.value = false
  }
}
// 計算プロパティ（セーフガード付き）
const completedCount = computed(() => {
  if (!Array.isArray(todos.value)) {
    return 0
  }
  return todos.value.filter(todo => todo.completed).length
})

const remainingCount = computed(() => {
  if (!Array.isArray(todos.value)) {
    return 0
  }
  return todos.value.filter(todo => !todo.completed).length
})

const progressPercentage = computed(() => {
  if (!Array.isArray(todos.value) || todos.value.length === 0) {
    return 0
  }
  return Math.round((completedCount.value / todos.value.length) * 100)
})

const addTodo = async () => {
  if (!newTodo.title.trim()) return

  loading.value = true
  const createdTodo = await createTodo({
    title: newTodo.title.trim(),
    description: newTodo.description.trim()
  })

  if (createdTodo) {
    todos.value.unshift(createdTodo) // 先頭に追加
    newTodo.title = ''
    newTodo.description = ''

    showSuccessMessage('Todoを追加しました！')
  }
  loading.value = false
}

const focusDescription = () => {
  nextTick(() => {
    descriptionInput.value?.focus()
  })
}

const showSuccessMessage = (message: string) => {
  successMessage.value = message
  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
}

const toggleTodo = async (todo: Todo) => {
  const updatedTodo = await updateTodo(todo.id, {
    completed: !todo.completed
  })

  if (updatedTodo) {
    const index = todos.value.findIndex(t => t.id === todo.id)
    if (index !== -1) {
      todos.value[index] = updatedTodo
    }
  }
}

const removeTodo = async (id: number) => {
  if (!confirm('このTodoを削除しますか？')) return

  const success = await deleteTodo(id)
  if (success) {
    todos.value = todos.value.filter(todo => todo.id !== id)
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ja-JP', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 初期データ読み込み
onMounted(() => {
  refreshTodos()
})
</script>
