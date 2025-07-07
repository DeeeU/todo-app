from rest_framework import serializers
from .models import Todo, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']

class TodoSerializer(serializers.ModelSerializer):
    """
    TodoモデルをJSON形式に変換するシリアライザー

    例：
    Todoオブジェクト → {"id": 1, "title": "買い物", "completed": false, ...}
    JSON → Todoオブジェクト
    """

    owner = UserSerializer(read_only=True)  # ネストしたユーザー情報を含める

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at', 'owner']
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']  # 読み取り専用（変更不可）
