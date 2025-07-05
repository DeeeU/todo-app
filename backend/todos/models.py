from django.db import models
from django.utils import timezone

class Todo(models.Model):
    title = models.CharField(max_length=200, db_index=True)  # タイトル検索用
    description = models.TextField(blank=True, default='')
    completed = models.BooleanField(default=False, db_index=True)  # 完了状態フィルター用
    created_at = models.DateTimeField(default=timezone.now, db_index=True)  # 並び替え用
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # 複合インデックス（よく一緒に使われる条件の組み合わせ）
        indexes = [
            models.Index(fields=['completed', 'created_at']),  # 完了状態 + 日付
            models.Index(fields=['title', 'completed']),       # タイトル + 完了状態
            models.Index(fields=['-created_at']),              # 作成日時降順（デフォルト並び）
        ]

    def __str__(self):
        return self.title
