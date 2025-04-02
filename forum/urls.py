from django.contrib import admin
from django.urls import path
import form
import form.views
import main.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",form.views.form,name='form'),
    path("main/",main.views.index,name='index'),
    path('login/',form.views.user_login,name='login'),
    path('create_post/',main.views.create_post,name='create_post'),
]
