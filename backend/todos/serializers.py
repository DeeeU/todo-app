from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    """
    TodoモデルをJSON形式に変換するシリアライザー

    例：
    Todoオブジェクト → {"id": 1, "title": "買い物", "completed": false, ...}
    JSON → Todoオブジェクト
    """
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']  # 読み取り専用（変更不可）
