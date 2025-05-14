from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
import form.views
import main.views
import form

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', form.views.user_login, name='login'),
    path('register/', form.views.form, name='form'),
    path('accounts/', include('allauth.urls')),
    path("main/", main.views.index, name='index'),
    path('logout/', main.views.user_logout, name='logout'),
    path('create_post/', main.views.create_post, name='create_post'),
    path('like/<slug:slug>/', main.views.like_dislike, name='like_dislike'),
    path("add_comment/<slug:slug>/", main.views.add_comment, name="add_comment"),
    path("delete_comment/", main.views.delete_comment, name="delete_comment"),
    path("edit_comment/", main.views.edit_comment, name="edit_comment"),
    path('update-avatar/', main.views.update_avatar, name='update_avatar'),
    path('post/<slug:slug>/', main.views.post_detail, name='post_detail'),
    path('search/', main.views.search_results, name='search_results'),
    path('check-category/', main.views.check_category, name='check_category'),
    path('category/<slug:slug>/', main.views.posts_by_category, name='posts_by_category'),
    path('post-counters/', main.views.post_counters, name='post_counters'),
    path('admin/delete_post/<slug:post_slug>/', main.views.admin_delete_post, name='admin_delete_post'),
    path('report/<slug:slug>/', main.views.report_post, name='report_post'),
    path('add-reply/', main.views.add_reply, name='add_reply'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
