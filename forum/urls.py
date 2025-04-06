from django.contrib import admin
from django.urls import path, include
import form
import form.views
import main.views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("",form.views.form,name='form'),
    path("main/",main.views.index,name='index'),
    path('login/',form.views.user_login,name='login'),
    path('logout/',main.views.user_logout,name='logout'),
    path('create_post/',main.views.create_post,name='create_post'),
    path('like/<int:post_id>/', main.views.like_dislike, name='like_dislike'),
    path("add_comment/", main.views.add_comment, name="add_comment"),
    path('profile/<str:username>/', main.views.profile_view, name='profile'),
    path("delete_comment/", main.views.delete_comment, name="delete_comment"),
    path("edit_comment/", main.views.edit_comment, name="edit_comment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
