from django.shortcuts import render, redirect
from django.contrib.auth import logout
from main.models import Post

def index(request):

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        # Створення нового поста
        post = Post(title=title, content=content, author=request.user)
        post.save()

    # Отримуємо всі пости з бази даних
    posts = Post.objects.all().order_by('-created_at')  # Сортуємо по даті створення (від найновіших)

    # Повертаємо шаблон з оновленими постами
    return render(request, "main/index.html", {'posts': posts})


def user_logout(request):
    logout(request)  # Викликаємо logout для виведення користувача
    return redirect('form') 

   
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        # Створення нового поста
        post = Post(title=title, content=content, author=request.user)
        post.save()

        # Повертаємо користувача на головну сторінку
        return redirect('index')  # Переходимо на головну сторінку

    return render(request, 'main/create_post.html')  # Повертаємо форму для створення поста