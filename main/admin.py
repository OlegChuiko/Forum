from main.models import Post, Comment, Like ,UserProfile,Dislike,Category
from django.contrib import admin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'category')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(UserProfile)
admin.site.register(Dislike)