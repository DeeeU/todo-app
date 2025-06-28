from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    """
    Todo の CRUD 操作を提供する API ビュー

    ModelViewSet が自動的に以下のエンドポイントを作成：
    - GET /api/todos/     → 全Todo一覧取得
    - POST /api/todos/    → 新しいTodo作成
    - GET /api/todos/{id}/ → 特定のTodo取得
    - PUT /api/todos/{id}/ → Todo全体更新
    - PATCH /api/todos/{id}/ → Todo部分更新
    - DELETE /api/todos/{id}/ → Todo削除
    """
    queryset = Todo.objects.all()  # 全てのTodoオブジェクトを取得
    serializer_class = TodoSerializer  # 使用するシリアライザーを指定
