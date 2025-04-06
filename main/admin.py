from django.contrib import admin
from main.models import Post, Comment, Like ,UserProfile,Dislike

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(UserProfile)
admin.site.register(Dislike)