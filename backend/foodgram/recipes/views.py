from django.core.paginator import Paginator

from .models import Recipe


RECIPES_PER_PAGE = 6


def index(request):
    """Calling main page with the latest recipes."""
    recipes = Recipe.objects.all().order_by('-pub_date')
    paginator = Paginator(recipes, RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
#     return render(request, 'posts/index.html', context)


# from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator
# from django.shortcuts import get_object_or_404, render, redirect
# from django.views.decorators.cache import cache_page
# 
# from .forms import CommentForm, PostForm
# from .models import Follow, Group, Post, User
# 
# POSTS_PER_PAGE = 10
# 
# 
# @cache_page(20)
# def index(request):
#     """Функция вызова главной страницы с последними постами."""
#     posts = Post.objects.all()
#     paginator = Paginator(posts, POSTS_PER_PAGE)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'page_obj': page_obj,
#     }
#     return render(request, 'posts/index.html', context)
# 
# 
# def group_posts(request, slug):
#     """Функция вызова страницы группы с постами группы."""
#     group = get_object_or_404(Group, slug=slug)
#     posts = group.posts.all()
#     paginator = Paginator(posts, POSTS_PER_PAGE)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'group': group,
#         'page_obj': page_obj,
#     }
#     return render(request, 'posts/group_list.html', context)
# 
# 
# def profile(request, username):
#     author = get_object_or_404(User, username=username)
#     user = request.user
#     following = user.is_authenticated and Follow.objects.filter(
#         user=user,
#         author=author,
#     ).exists()
#     posts = author.posts.all()
#     paginator = Paginator(posts, POSTS_PER_PAGE)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     posts_count = posts.count()
#     context = {
#         'page_obj': page_obj,
#         'posts_count': posts_count,
#         'author': author,
#         'following': following,
#     }
#     return render(request, 'posts/profile.html', context)
# 
# 
# def post_detail(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     comments = post.comments.all()
#     form = CommentForm()
#     author = post.author
#     posts_count = author.posts.count()
#     context = {
#         'post': post,
#         'posts_count': posts_count,
#         'comments': comments,
#         'form': form,
#     }
#     return render(request, 'posts/post_detail.html', context)
# 
# 
# @login_required()
# def post_create(request):
#     template = 'posts/create_post.html'
#     form = PostForm(
#         request.POST or None,
#         files=request.FILES or None,
#     )
#     if form.is_valid():
#         post = form.save(False)
#         post.author = request.user
#         post.save()
#         return redirect('posts:profile', username=request.user.username)
#     context = {
#         'form': form,
#         'is_edit': False,
#     }
#     return render(request, template, context)
# 
# 
# @login_required
# def post_edit(request, post_id):
#     template = 'posts/create_post.html'
#     post = get_object_or_404(Post, id=post_id)
#     form = PostForm(instance=post)
#     if request.user != post.author:
#         return redirect('posts:post_detail', post_id=post_id)
#     form = PostForm(
#         request.POST or None,
#         files=request.FILES or None,
#         instance=post,
#     )
#     if form.is_valid():
#         post.save()
#         return redirect('posts:post_detail', post_id=post_id)
#     context = {
#         'form': form,
#         'is_edit': True,
#     }
#     return render(request, template, context)
# 
# 
# @login_required
# def add_comment(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     form = CommentForm(request.POST or None)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.author = request.user
#         comment.post = post
#         comment.save()
#     return redirect('posts:post_detail', post_id=post_id)
# 
# 
# @login_required
# def follow_index(request):
#     user = request.user
#     posts = Post.objects.filter(author__following__user=user)
#     paginator = Paginator(posts, POSTS_PER_PAGE)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'page_obj': page_obj,
#     }
#     return render(request, 'posts/follow.html', context)
# 
# 
# @login_required
# def profile_follow(request, username):
#     author = get_object_or_404(User, username=username)
#     user = request.user
#     if author != user:
#         Follow.objects.get_or_create(user=user, author=author)
#     return redirect('posts:profile', username=username)
# 
# 
# @login_required
# def profile_unfollow(request, username):
#     author = get_object_or_404(User, username=username)
#     user = request.user
#     follow = Follow.objects.filter(user=user, author=author)
#     if follow.exists():
#         follow.delete()
#     return redirect('posts:profile', username=username)