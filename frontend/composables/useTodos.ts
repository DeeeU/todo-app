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

  const fetchTodos = async (): Promise<Todo[]> => {
    try {
      const data = await $fetch<Todo[]>(`${apiBase}/todos/`)
      return data
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
