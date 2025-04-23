from django.shortcuts import get_object_or_404, render, redirect
from main.models import Post, Like, Dislike,Comment, UserProfile
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from forum import settings
import bleach
import random


def get_random_recent_posts(count=3, days=7):
    recent_posts = Post.objects.filter(created_at__gte=timezone.now() - timedelta(days=days))
    recent_posts_list = list(recent_posts)

    if len(recent_posts_list) < count:
        all_posts = list(Post.objects.all())
        return random.sample(all_posts, min(count, len(all_posts)))

    return random.sample(recent_posts_list, count)

random_posts = get_random_recent_posts()

@login_required()
def index(request):
     
    all_posts = Post.objects.annotate(
    comment_count=Count('comments'),
    like_count=Count('likes')
    )

    recent_list = all_posts.order_by('-created_at')
    most_response_list = all_posts.filter(comment_count__gt=0).order_by('-comment_count', '-created_at')
    no_response_list = all_posts.filter(comment_count=0).order_by('-created_at')
    popular_list = all_posts.order_by('-like_count', '-created_at')

    page_number = request.GET.get('page')

    recent_paginator = Paginator(recent_list, 5)
    most_response_paginator = Paginator(most_response_list, 5)
    no_response_paginator = Paginator(no_response_list, 5)
    popular_paginator = Paginator(popular_list, 5)

    user = request.user
    post_count = Post.objects.filter(author=user).count()
    comment_count = Comment.objects.filter(author=user).count()

    context = {
        'recent_posts': recent_paginator.get_page(page_number),
        'most_response_posts': most_response_paginator.get_page(page_number),
        'no_response_posts': no_response_paginator.get_page(page_number),
        'popular_posts': popular_paginator.get_page(page_number),
        'random_posts': random_posts,
        'post_count': post_count,
        'comment_count': comment_count
    }

    return render(request, 'main/index.html', context)

@login_required()
def user_logout(request):
    logout(request)  
    return redirect('login')

@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        image = request.FILES.get("image")
        audio = request.FILES.get("audio")

        ALLOWED_TAGS = [
            'p', 'br', 'b', 'i', 'u', 'em', 'strong', 'ul', 'ol', 'li', 'span'
        ]
        ALLOWED_ATTRIBUTES = {
            'span': ['style'],
        }

        raw_content = request.POST.get("content") 

        clean_content = bleach.clean(
            raw_content,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )

        post = Post(
            title=title,
            content=clean_content,
            author=request.user,
            image=image,
            audio=audio
        )
        post.save()
        return redirect('index')
    user = request.user
    post_count = Post.objects.filter(author=user).count()
    comment_count = Comment.objects.filter(author=user).count()

    return render(request, 'main/create_post.html',{'random_posts': random_posts,'post_count':post_count,'comment_count':comment_count})

@login_required()
def like_dislike(request, slug):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated."}, status=401)

    post = get_object_or_404(Post, slug=slug)
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
def add_comment(request, slug):
    content = request.POST.get("content")

    if not content:
        return JsonResponse({"error": "Некоректні дані"}, status=400)

    post = get_object_or_404(Post, slug=slug)
    comment = Comment.objects.create(post=post, author=request.user, content=content)

    avatar_url = ""
    social_account = SocialAccount.objects.filter(user=request.user).first()
    if social_account and social_account.get_avatar_url():
        avatar_url = social_account.get_avatar_url()
    elif hasattr(request.user, "userprofile") and request.user.userprofile.avatar:
        avatar_url = request.user.userprofile.avatar.url
    else:
        avatar_url = settings.DEFAULT_AVATAR_URL 

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


@login_required
def update_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.avatar = request.FILES['avatar']
        profile.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required()
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = None  

        if user_profile and not user_profile.viewed_posts.filter(id=post.id).exists():
            post.views += 1
            post.save()

            user_profile.viewed_posts.add(post)

    user = request.user
    post_count = Post.objects.filter(author=user).count()
    comment_count = Comment.objects.filter(author=user).count()

    related_posts = Post.objects.filter(author=post.author)\
        .exclude(id=post.id)\
        .order_by('-created_at')[:4]
    
    return render(request, 'main/post-details.html', {
        'post': post,
        'comments': comments,
        'random_posts': random_posts,
        'post_count':post_count,
        'comment_count':comment_count,
        'related_posts': related_posts
    })

@login_required()
def search_results(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        results = Post.objects.filter(title__icontains=query) 

    return render(request, 'main/search.html', {
        'results': results,
        'query': query
    })

