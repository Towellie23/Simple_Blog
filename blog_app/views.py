from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, CommentForm


def post_listing(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_listing.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form, 'comments': comments})


    # post = get_object_or_404(Post, id=id)
    # return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
        else:
            return render(request, 'blog/post_form.html', {'form': form})

def about(request):
    return render(request, 'blog/about.html')

