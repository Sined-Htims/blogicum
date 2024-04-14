from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, AccessMixin
)
from django.db.models import Count
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Post, Comments
from .forms import PostForm, CommentsForm, UserUpdateForm

User = get_user_model()


class SuperuserOrAuthorMixin(UserPassesTestMixin, AccessMixin):
    def test_func(self):
        self.object = self.get_object()
        if '/profile/' in self.request.path:
            return self.request.user.username == self.object.username
        else:
            return self.request.user == self.object.author

    def handle_no_permission(self, **kwargs):
        if '/profile/' in self.request.path:
            return redirect('blog:profile', self.kwargs['username'])
        else:
            return redirect('blog:post_detail', self.kwargs['post_id'])


class PostsListView(ListView):
    model = Post
    paginate_by = 10
    queryset = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=timezone.now()
    ).annotate(comment_count=Count('comments')).order_by(
        '-pub_date'
    )


class PostsDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        form = CommentsForm()
        context = super().get_context_data(**kwargs)
        context.update({'form': form})
        context['comments'] = Comments.objects.select_related(
            'post', 'author',
        ).filter(
            post=self.kwargs['post_id']
        )
        return context

    def get_queryset(self, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        queryset = Post.objects.select_related(
            'location',
            'author',
            'category'
        ).filter(pk=self.kwargs['post_id'])
        if post.author == self.request.user:
            return queryset
        else:
            return queryset.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lt=timezone.now(),
            )


class PostsCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostsUpdateView(LoginRequiredMixin, SuperuserOrAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(LoginRequiredMixin, SuperuserOrAuthorMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/post_form.html'
    context_object_name = 'form'
    success_url = reverse_lazy('blog:index')


class CategoryListView(ListView):
    paginate_by = 10
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.values(
                'title',
                'description',
                'slug',
                'is_published',
            ).filter(is_published=True),
            slug=self.kwargs['category_slug']
        )
        return context

    def get_queryset(self):
        return Post.objects.select_related(
            'location',
            'author',
            'category'
        ).filter(
            is_published=True,
            category__is_published=True,
            category__slug=self.kwargs['category_slug'],
            pub_date__lt=timezone.now()
        ).annotate(
            comment_count=Count('comments')
        ).order_by(
            '-pub_date'
        )


class ProfileListView(ListView):
    model = User
    paginate_by = 10
    template_name = 'blog/profile_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User.objects.all(),
            username=self.kwargs['username']
        )
        return context

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs['username'])
        queryset = Post.objects.select_related(
            'location',
            'author',
            'category'
        ).annotate(
            comment_count=Count('comments')
        ).order_by(
            '-pub_date'
        )
        if user == self.request.user:
            return queryset.filter(author_id__username=self.kwargs['username'])
        else:
            return queryset.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lt=timezone.now(),
                author_id__username=self.kwargs['username']
            )


class ProfileUpdateView(
    LoginRequiredMixin, SuperuserOrAuthorMixin, UpdateView
):
    model = User
    form_class = UserUpdateForm
    slug_url_kwarg = 'username'
    slug_field = 'username'
    template_name = 'blog/user.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.object.username}
        )


@login_required
def add_comment(request, post_id, comment_id=None,):
    post = get_object_or_404(Post, pk=post_id)
    if comment_id is not None:
        instance = get_object_or_404(Comments, pk=comment_id)
        if instance.author != request.user:
            return redirect('blog:post_detail', post_id)
    else:
        instance = None
    form = CommentsForm(request.POST or None, instance=instance)
    context = {'form': form, 'post': post, 'comment': instance}
    if form.is_valid():
        comments = form.save(commit=False)
        comments.author = request.user
        comments.post = post
        comments.save()
        return redirect('blog:post_detail', post_id=post.id)
    return render(request, 'blog/comment.html', context)


class CommentsDeleteView(
    LoginRequiredMixin, SuperuserOrAuthorMixin, DeleteView
):
    model = Comments
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = get_object_or_404(Comments, pk=self.kwargs['comment_id'])
        context['comment'] = comment
        return context

    # def dispatch(self, request, *args, **kwargs):
    #     post_id = self.kwargs['post_id']
    #     comment = get_object_or_404(Comments, pk=self.kwargs['comment_id'])
    #     if request.user.is_authenticated:
    #         if comment.author == self.request.user:
    #             return super().dispatch(request, *args, **kwargs)
    #     return redirect('blog:post_detail', post_id)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )
