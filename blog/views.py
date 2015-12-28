from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.http import Http404

from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from blog.models import Category
from blog.models import Post
from blog.models import Comment

from blog.forms import PostForm
from blog.forms import CommentForm

from django.contrib.auth import get_user_model

User = get_user_model()



def index(request):
    count = request.session.get('index_page_count', 0) + 1
    request.session['index_page_count'] = count

    post_list = Post.objects.all()

    return render(request, 'blog/index.html', {
        'count': count,
        'post_list': post_list,
    })



def detail(request, pk=None, uuid=None):
    if pk:
        post = get_object_or_404(Post, pk=pk)
    elif uuid:
        post = get_object_or_404(Post, uuid=uuid)
    else:
        raise Http404

    return render(request, 'blog/detail.html', {
        'post': post,
    })



@login_required
def new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Created Successfully.')
            return redirect(post)
    else:
        form = PostForm()
    return render(request, 'form.html', {
        'form': form,
    })



@login_required
def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Updated Successfully.')
            return redirect(post)
    else:
        form = PostForm(instance=post)
    return render(request, 'form.html', {
        'form': form,
    })



@login_required
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Deleted Successfully.')
        return redirect('blog:index')
    return render(request, 'comment_delete_confirm.html', {
        'comment': comment,
    })



@login_required
def comment_new(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = get_object_or_404(Post, pk=pk)
            comment.save()
            messages.success(request, 'Created Successfully.')
            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(request, 'form.html', {
        'form': form,
    })



@login_required
def comment_edit(request, post_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully.')
            return redirect(comment.post)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'form.html', {
        'form': form,
    })



@login_required
def comment_delete(request, post_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Deleted Successfully.')
        return redirect(comment.post)
    return render(request, 'comment_delete_confirm.html', {
        'comment': comment,
    })


