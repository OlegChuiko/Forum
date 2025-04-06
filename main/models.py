from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)  # Назва поста
    content = models.TextField()  # Текст поста
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор поста (зв'язок з User)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата і час створення поста
    updated_at = models.DateTimeField(auto_now=True)  # Дата і час останнього оновлення поста
    likes = models.IntegerField(default=0)  # Кількість лайків
    dislikes = models.PositiveIntegerField(default=0)  # Кількість дизлайків
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    audio = models.FileField(upload_to='posts/audio/', null=True, blank=True)
    
    def __str__(self):
        return self.title  # Назва поста як представлення моделі

    def update_like_count(self):
        """ Оновлення кількості лайків і дизлайків для поста """
        self.likes = self.like_set.count()
        self.dislikes = self.dislike_set.count()
        self.save()

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
    
class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Зв'язок з постом
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Користувач, який поставив дизлайк
    created_at = models.DateTimeField(auto_now_add=True)  # Дата і час дизлайку
    
    class Meta:
        unique_together = ('post', 'user')  # Один користувач може поставити дизлайк лише один раз на пост

    def __str__(self):
        return f"Dislike by {self.user.username} on {self.post.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')

    def __str__(self):
        return f"{self.user.username} Profile"