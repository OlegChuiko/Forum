from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)  # Назва поста
    content = models.TextField()  # Текст поста
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор поста (зв'язок з User)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата і час створення поста
    updated_at = models.DateTimeField(auto_now=True)  # Дата і час останнього оновлення поста
    likes = models.IntegerField(default=0)  # Кількість лайків
    dislikes = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title  # Назва поста як представлення моделі

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")  # Зв'язок з постом
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор коментаря
    content = models.TextField()  # Текст коментаря
    created_at = models.DateTimeField(auto_now_add=True)  # Дата і час створення коментаря
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Зв'язок з постом
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Користувач, який поставив лайк
    created_at = models.DateTimeField(auto_now_add=True)  # Дата і час лайку
    
    class Meta:
        unique_together = ('post', 'user')  # Один користувач може поставити лайк лише один раз на пост

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"

