from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Rating
from .forms import PostForm, CommentForm, UserRegisterForm, RatingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Avg

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})




def post_listing(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_listing.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter(parent__isnull=True)
    comment_form = CommentForm()  # Инициализация формы комментария
    rating_form = RatingForm()    # Инициализация формы рейтинга

    if request.method == 'POST':
        if 'comment_form' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post_detail', id=post.id)
        elif 'rating_form' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.post = post
                rating.user = request.user
                rating.save()
                return redirect('post_detail', id=post.id)

    average_rating = post.ratings.aggregate(Avg('score'))['score__avg']

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
        'rating_form': rating_form,
        'average_rating': average_rating,
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit(request, id):
    # Получаем пост по id или возвращаем 404, если пост не найден
    post = get_object_or_404(Post, id=id)

    # Проверяем, что текущий пользователь является автором поста
    if request.user != post.author:
        return redirect('home')

    # Обработка POST-запроса (отправка формы)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        # Обработка GET-запроса (отображение формы)
        form = PostForm(instance=post)

    # Передаем форму и пост в контекст шаблона
    return render(request, 'blog/post_form.html', {'form': form, 'post': post})


def about(request):
    return render(request, 'blog/about.html')

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        return redirect('home')
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})