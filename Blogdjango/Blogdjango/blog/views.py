from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, PostForm
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

def post_list_view(request):
    posts = Post.objects.filter(published=True).order_by('-pub_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, published=True)
    return render(request, 'blog/post_detail.html', {'post': post})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Добро пожаловать, {username}! Ваш аккаунт был успешно создан.')
            login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    return redirect('post_list')

@login_required
def profile_view(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-pub_date')
    return render(request, 'blog/profile.html', {'posts': user_posts})

@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Связывае пост с текущим пользователем
            post.save()
            messages.success(request, 'Пост успешно создан!')
            return redirect('post_detail', post_id=post.id)  # Перенаправление на детальный просмотр поста
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Проверка что текущий пользователь является автором поста
    if post.author != request.user:
        messages.error(request, 'У вас нет прав для редактирования этого поста.')
        return redirect('post_detail', post_id=post.id)

    # Обработка POST-запроса (сохранение изменений)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успешно обновлен!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)

    return render(request, 'blog/profile.html', {'user': user, 'posts': posts})

@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)


    if post.author != request.user:
        return HttpResponseForbidden('У вас нет прав для удаления этого поста.')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост успешно удален.')
        return redirect('post_list')

    return render(request, 'blog/confirm_delete.html', {'post': post})