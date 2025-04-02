from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from main.models import Post, Comment

def index(request):
    posts = Post.objects.all().order_by('-created_at')

    # Додати коментар
    if request.method == 'POST' and 'comment_content' in request.POST:
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        comment_content = request.POST.get('comment_content')
        
        # Створити новий коментар
        Comment.objects.create(post=post, author=request.user, content=comment_content)
        
        return redirect('index')  # Повертаємо на головну сторінку

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