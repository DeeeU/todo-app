from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Todo(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, default='')
    completed = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # リレーション追加（外部キー）
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='todos',
        default=1  # デフォルトでID=1のユーザーを設定
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'completed']),       # ユーザー + 完了状態
            models.Index(fields=['owner', 'created_at']),      # ユーザー + 作成日時
            models.Index(fields=['completed', 'created_at']),  # 完了状態 + 日付
            models.Index(fields=['title', 'completed']),       # タイトル + 完了状態
            models.Index(fields=['-created_at']),              # 作成日時降順
        ]

    def __str__(self):
        return f"{self.title} (by {self.owner.name})"
