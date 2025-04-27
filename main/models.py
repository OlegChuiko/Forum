from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from unidecode import unidecode
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=200) 
    content = models.TextField()  
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now) 
    slug = models.SlugField(unique=True,blank=True,null=True)
    likes = models.IntegerField(default=0) 
    dislikes = models.PositiveIntegerField(default=0) 
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    audio = models.FileField(upload_to='posts/audio/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.title))
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title  

    def update_like_count(self):
        """ Оновлення кількості лайків і дизлайків для поста """
        self.likes = self.like_set.count()
        self.dislikes = self.dislike_set.count()
        self.save()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()  
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('post', 'user')  

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"
    
class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(default=timezone.now)  
    
    class Meta:
        unique_together = ('post', 'user')  

    def __str__(self):
        return f"Dislike by {self.user.username} on {self.post.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    viewed_posts = models.ManyToManyField(Post, related_name='viewed_by', blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
    