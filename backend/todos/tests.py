# todos/tests.py
from django.test import TestCase
from django.utils import timezone
from .models import Todo
from rest_framework.test import APITestCase
from rest_framework import status

class TodoModelTest(TestCase):
    """Todoモデルのテスト"""

    def setUp(self):
        """各テストの前に実行される準備処理"""
        self.todo = Todo.objects.create(
            title="テスト用Todo",
            description="テスト用の説明",
            completed=False
        )

    def test_todo_creation(self):
        """Todoが正しく作成されることをテスト"""
        self.assertEqual(self.todo.title, "テスト用Todo")
        self.assertEqual(self.todo.description, "テスト用の説明")
        self.assertFalse(self.todo.completed)
        self.assertIsNotNone(self.todo.created_at)
        self.assertIsNotNone(self.todo.updated_at)

    def test_todo_str_method(self):
        """__str__メソッドが正しく動作することをテスト"""
        self.assertEqual(str(self.todo), "テスト用Todo")

    def test_todo_default_values(self):
        """デフォルト値が正しく設定されることをテスト"""
        new_todo = Todo.objects.create(title="最小限のTodo")
        self.assertEqual(new_todo.description, None)
        self.assertFalse(new_todo.completed)
        self.assertIsNotNone(new_todo.created_at)

    def test_todo_completion_toggle(self):
        """Todoの完了状態を変更できることをテスト"""
        # 初期状態は未完了
        self.assertFalse(self.todo.completed)

        # 完了状態に変更
        self.todo.completed = True
        self.todo.save()

        # データベースから再取得して確認
        updated_todo = Todo.objects.get(id=self.todo.id)
        self.assertTrue(updated_todo.completed)

    def test_todo_ordering(self):
        """Todoが作成日時の降順で並ぶことをテスト"""
        # 新しいTodoを作成
        newer_todo = Todo.objects.create(
            title="新しいTodo",
            description="後から作成"
        )

        # 全Todoを取得
        todos = Todo.objects.all()

        # 新しいものが最初に来ることを確認
        self.assertEqual(todos.first(), newer_todo)
        self.assertEqual(todos.last(), self.todo)

class TodoAPITest(APITestCase):

  def setUp(self):
    self.todo_data = {
        'title': 'APIテスト用Todo',
        'description': '説明',
        'completed': False
    }
    self.todo = Todo.objects.create(**self.todo_data)

  def test_get_todo_list(self):
      url = '/api/todos/'
      response = self.client.get(url)

      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data[0]['title'], 'APIテスト用Todo')
      self.assertEqual(response.data[0]['id'], self.todo.id)


  def test_update_todo(self):
      url = f'/api/todos/{self.todo.id}/'
      updated_todo_data = {
          'title': '更新されたTodo',
          'description': '更新された説明',
          'completed': True
      }
      response = self.client.put(url, updated_todo_data, format='json')

      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data['title'], updated_todo_data['title'])
      self.assertEqual(response.data['description'], updated_todo_data['description'])
      self.assertTrue(response.data['completed'])

      # データベースから再取得して確認
      updated_todo = Todo.objects.get(id=self.todo.id)
      self.assertEqual(updated_todo.title, updated_todo_data['title'])
      self.assertEqual(updated_todo.description, updated_todo_data['description'])
      self.assertTrue(updated_todo.completed)

  def test_partial_update_todo(self):
      url = f'/api/todos/{self.todo.id}/'
      partial_data = { 'completed': True }
      response = self.client.patch(url, partial_data, format='json')

      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertTrue(response.data['completed'])
      # タイトルは変更されない
      self.assertEqual(response.data['title'], 'APIテスト用Todo')


  def test_delete_todo(self):
      url = f'/api/todos/{self.todo.id}/'
      response = self.client.delete(url)

      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      self.assertEqual(Todo.objects.count(), 0)

  def test_create_todo_validation(self):
      url = '/api/todos/'
      invalid_data = {
          'title': '',  # タイトルが空
          'description': '失敗'
      }
      response = self.client.post(url, invalid_data, format='json')

      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      self.assertIn('title', response.data)  # タイトルのエラーが含まれることを確認
      self.assertEqual(Todo.objects.count(), 1)  # 元のTodoは削除されていない
