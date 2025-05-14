from main.models import Post, Comment, Like ,UserProfile,Dislike,Category,Report
from django.utils.html import format_html
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

class ReportAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'reported_by', 'reason', 'created_at', 'view_post', 'delete_post')
    search_fields = ('post__title', 'reported_by__username', 'reason')
    list_filter = ('created_at',)

    def post_title(self, obj):
        return obj.post.title
    post_title.short_description = 'Пост'

    def view_post(self, obj):
        return format_html('<a href="/admin/main/post/{}/change/" target="_blank">🔍 Переглянути</a>', obj.post.id)
    view_post.short_description = 'Перегляд поста'

    def delete_post(self, obj):
        return format_html(
            '<a href="/admin/delete_post/{}/" onclick="return confirm(\'Ви впевнені, що хочете видалити цей пост?\')">🗑 Видалити пост</a>',
            obj.post.slug
        )
    delete_post.short_description = 'Видалити пост'

admin.site.register(Report, ReportAdmin)

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(UserProfile)
admin.site.register(Dislike)