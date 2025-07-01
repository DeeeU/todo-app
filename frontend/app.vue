<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold mb-4">🔍 デバッグモード</h1>

    <button
      @click="testFetch"
      class="bg-blue-500 text-white px-4 py-2 rounded mb-4"
    >
      APIを直接テスト
    </button>

    <div class="bg-gray-100 p-4 rounded">
      <h2 class="font-bold">結果:</h2>
      <p><strong>データ型:</strong> {{ dataType }}</p>
      <p><strong>配列か:</strong> {{ isArray }}</p>
      <p><strong>件数:</strong> {{ count }}</p>
      <p><strong>最初の要素:</strong></p>
      <pre class="bg-white p-2 rounded mt-2 text-sm">{{ firstItem }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
const { fetchTodos } = useTodos()

const dataType = ref('')
const isArray = ref(false)
const count = ref(0)
const firstItem = ref(null)

const testFetch = async () => {
  console.log('=== 直接テスト開始 ===')

  const result = await fetchTodos()

  dataType.value = typeof result
  isArray.value = Array.isArray(result)
  count.value = result?.length || 0
  firstItem.value = result?.[0] || null

  console.log('=== テスト結果 ===')
  console.log('型:', typeof result)
  console.log('配列:', Array.isArray(result))
  console.log('件数:', result?.length)
  console.log('生データ:', result)
}
</script>
