from time import localtime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from main.models import Post, Like, Dislike,Comment
from django.contrib.auth.models import User
from django.templatetags.static import static


from allauth.socialaccount.models import SocialAccount

@login_required()
def index(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        content = request.POST.get("comment_content")

        if post_id and content:
            post = get_object_or_404(Post, id=post_id)
            Comment.objects.create(post=post, author=request.user, content=content)
            return redirect('index')  # оновлення сторінки після коментаря

    posts = Post.objects.all().prefetch_related('like_set', 'dislike_set', 'comments')

    for post in posts:
        post.user_liked = post.like_set.filter(user=request.user).exists()
        post.user_disliked = post.dislike_set.filter(user=request.user).exists()
        post.likes = post.like_set.count()
        post.dislikes = post.dislike_set.count()

    return render(request, 'main/index.html', {'posts': posts})


def user_logout(request):
    logout(request)  
    return redirect('form')

@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get('image')
        audio = request.FILES.get('audio')  # Audio

        post = Post(
            title=title,
            content=content,
            author=request.user,
            image=image,
            audio=audio
        )
        post.save()
        return redirect('index')
    
    return render(request, 'main/create_post.html')

def like_dislike(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated."}, status=401)

    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action')

        if action not in ['like', 'dislike']:
            return JsonResponse({"error": "Invalid action."}, status=400)

        liked = Like.objects.filter(post=post, user=user)
        disliked = Dislike.objects.filter(post=post, user=user)

        if action == 'like':
            if disliked.exists():
                disliked.delete()
                post.dislikes -= 1
            if liked.exists():
                liked.delete()
                post.likes -= 1
            else:
                Like.objects.create(post=post, user=user)
                post.likes += 1

        elif action == 'dislike':
            if liked.exists():
                liked.delete()
                post.likes -= 1
            if disliked.exists():
                disliked.delete()
                post.dislikes -= 1
            else:
                Dislike.objects.create(post=post, user=user)
                post.dislikes += 1

        post.save()

        return JsonResponse({"likes": post.likes, "dislikes": post.dislikes})
    
    return JsonResponse({"error": "Invalid request."}, status=400)

@login_required()
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'main/profile.html', {
        'profile_user': user,
        'posts': posts,
    })

@require_POST
@login_required
def add_comment(request):
    post_id = request.POST.get("post_id")
    content = request.POST.get("content")

    if not post_id or not content:
        return JsonResponse({"error": "Некоректні дані"}, status=400)

    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(post=post, author=request.user, content=content)

    # Отримуємо аватарку
    avatar_url = ""
    social_account = SocialAccount.objects.filter(user=request.user).first()
    if social_account and social_account.get_avatar_url():
        avatar_url = social_account.get_avatar_url()
    elif hasattr(request.user, "userprofile") and request.user.userprofile.avatar:
        avatar_url = request.user.userprofile.avatar.url
    else:
        avatar_url = static('avatars/default.png')  # default avatar

    return JsonResponse({
        "comment_id": comment.id,
        "author": comment.author.username,
        "content": comment.content,
        "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
        "avatar_url": avatar_url,
        "is_owner": True  
    })

@require_POST
@login_required
def delete_comment(request):
    comment_id = request.POST.get('comment_id')

    try:
        comment = Comment.objects.get(id=comment_id)

        if comment.author != request.user:
            return JsonResponse({'error': 'Ви не можете видалити цей коментар.'}, status=403)

        comment.delete()
        return JsonResponse({'success': True})

    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Коментар не знайдено.'}, status=404)

@require_POST
@login_required
def edit_comment(request):
    comment_id = request.POST.get('comment_id')
    content = request.POST.get('content')

    try:
        comment = Comment.objects.get(id=comment_id)

        if comment.author != request.user:
            return JsonResponse({'error': 'Ви не можете редагувати цей коментар.'}, status=403)

        comment.content = content
        comment.save()
        return JsonResponse({'success': True, 'updated_content': comment.content})

    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Коментар не знайдено.'}, status=404)
