from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy

from django.shortcuts import get_object_or_404
from django.shortcuts import resolve_url

from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from blog.models import Post
from blog.models import Comment

from blog.forms import PostForm
from blog.forms import CommentForm

from instablog.thumbnail import make_thumbnail

User = get_user_model()



class AuthorListView(ListView):
    model = User
    context_object_name = 'list'
    template_name = 'blog/author_list.html'

author_list = AuthorListView.as_view()



class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'

index = PostListView.as_view()



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, *args, **kwargs):
        if 'uuid' in self.kwargs:
            return get_object_or_404(Post, uuid=self.kwargs['uuid'])
        return super(PostDetailView, self).get_object(*args, **kwargs)

detail = PostDetailView.as_view()



class PostCreateView(SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'form.html'
    success_message = "Created Successfully."

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object = form.save()
        make_thumbnail(self.object.photo.path, 400, 400)
        return super(PostCreateView, self).form_valid(form)

new = login_required(PostCreateView.as_view())



class PostUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'form.html'
    success_message = "Updated Successfully."

edit = login_required(PostUpdateView.as_view())



class PostDeleteView(DeleteView):
    model = Post
    template_name = 'comment_delete_confirm.html'
    success_message = "Deleted Successfully."
    success_url = reverse_lazy('blog:index')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

delete = login_required(PostDeleteView.as_view())



class CommentCreateView(SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'form.html'
    success_message = "Created Successfully."


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
        return resolve_url(self.object.post)

comment_new = login_required(CommentCreateView.as_view())



class CommentUpdateView(SuccessMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'form.html'
    success_message = "Updated Successfully."


    def get_success_url(self):
        return resolve_url(self.object.post)

comment_edit = login_required(CommentUpdateView.as_view())



class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment_delete_confirm.html'
    success_message = "Deleted Successfully."


    def get_success_url(self):
        return resolve_url(self.object.post)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CommentDeleteView, self).delete(request, *args, **kwargs)

comment_delete = login_required(CommentDeleteView.as_view())



class AuthorHomeView(ListView):
    model = Post
    template_name = 'blog/author_post_list.html'


    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        qs = super(AuthorHomeView, self).get_queryset()
        return qs.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super(AuthorHomeView, self).get_context_data(**kwargs)
        context['author'] = self.author
        return context

author_home = AuthorHomeView.as_view()


