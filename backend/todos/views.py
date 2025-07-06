from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    """
    Todo の CRUD 操作 + 検索機能を提供する API ビュー

    検索パラメータ:
    - search: タイトルでの部分一致検索
    - completed: 完了状態での絞り込み（true/false）

    使用例:
    GET /api/todos/?search=買い物
    GET /api/todos/?completed=true
    GET /api/todos/?search=プログラミング&completed=false
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        """
        クエリパラメータに基づいてTodoを絞り込み
        """
        queryset = Todo.objects.all()

        # 検索クエリ（タイトルでの部分一致）
        search_query = self.request.query_params.get('search', None)
        if search_query:

            queryset = queryset.filter(
                Q(title__icontains=search_query) |  # タイトルに含まれる
                Q(description__icontains=search_query)  # または説明に含まれる
            )

        # 完了状態での絞り込み
        completed_param = self.request.query_params.get('completed', None)
        if completed_param is not None:
            # 文字列 'true'/'false' をbooleanに変換
            completed_bool = completed_param.lower() == 'true'
            # インデックスを活用した高速絞り込み
            queryset = queryset.filter(completed=completed_bool)

        # デフォルトの並び順（最新順）はmodels.pyのMetaで設定済み
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Todo一覧取得 + 検索結果の統計情報付き
        """
        queryset = self.get_queryset()

        # ページネーション適用前の統計取得
        total_count = queryset.count()
        completed_count = queryset.filter(completed=True).count()

        # 通常のリスト取得処理
        response = super().list(request, *args, **kwargs)

        # レスポンスに統計情報を追加
        response.data = {
            'results': response.data,
            'meta': {
                'total_count': total_count,
                'completed_count': completed_count,
                'pending_count': total_count - completed_count,
                'search_query': request.query_params.get('search', ''),
                'completed_filter': request.query_params.get('completed', None)
            }
        }

        return response
