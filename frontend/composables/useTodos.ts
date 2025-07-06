export interface Todo {
  id: number
  title: string
  description: string
  completed: boolean
  created_at: string
  updated_at: string
}

export const useTodos = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  const fetchTodos = async (params: Record<string, string> = {}): Promise<Todo[]> => {
    try {
      const searchParams = new URLSearchParams(params)
      const queryString = searchParams.toString()
      const url = queryString
        ? `${apiBase}/todos/?${queryString}`
        : `${apiBase}/todos/`

      console.log('API呼び出し開始:', url)
      const data = await $fetch<any>(url)

      const todos = data.results || data
      const meta = data.meta

      console.log('API応答（型）:', typeof todos)
      console.log('API応答（配列か）:', Array.isArray(todos))
      console.log('API応答（件数）:', todos?.length)

      if (meta) {
        console.log('検索統計:', {
          total: meta.total_count,
          completed: meta.completed_count,
          pending: meta.pending_count,
          query: meta.search_query
        })
      }

      if (!Array.isArray(todos)) {
        console.error('APIの応答が配列ではありません:', todos)
        return []
      }

      return todos
    } catch (error) {
      console.error('Todo取得エラー:', error)
      return []
    }
  }

  const createTodo = async (todo: { title: string; description: string }): Promise<Todo | null> => {
    try {
      const data = await $fetch<Todo>(`${apiBase}/todos/`, {
        method: 'POST',
        body: {
          title: todo.title,
          description: todo.description,
          completed: false
        }
      })
      return data
    } catch (error) {
      console.error('Todo作成エラー:', error)
      return null
    }
  }

  const updateTodo = async (id: number, updates: Partial<Todo>): Promise<Todo | null> => {
    try {
      const data = await $fetch<Todo>(`${apiBase}/todos/${id}/`, {
        method: 'PATCH',
        body: updates
      })
      return data
    } catch (error) {
      console.error('Todo更新エラー:', error)
      return null
    }
  }

  const deleteTodo = async (id: number): Promise<boolean> => {
    try {
      await $fetch(`${apiBase}/todos/${id}/`, {
        method: 'DELETE'
      })
      return true
    } catch (error) {
      console.error('Todo削除エラー:', error)
      return false
    }
  }

  return {
    fetchTodos,
    createTodo,
    updateTodo,
    deleteTodo
  }
}
