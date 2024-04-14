from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from django.shortcuts import redirect


class SuperuserOrAuthorMixin(UserPassesTestMixin, AccessMixin):
    def test_func(self):
        self.object = self.get_object()
        if '/profile/' in self.request.path:
            return self.request.user.username == self.object.username
        return self.request.user == self.object.author

    def handle_no_permission(self, **kwargs):
        if '/profile/' in self.request.path:
            return redirect('blog:profile', self.kwargs['username'])
        return redirect('blog:post_detail', self.kwargs['post_id'])
