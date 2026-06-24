from django.shortcuts import render
from django.views.generic import UpdateView
from .forms import ProfileModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
# Create your views here.


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileModelForm
    template_name = "chat/profile_update.html"
    model = Profile
    slug_field = 'username'
    slug_url_kwarg = 'username'
    success_url = reverse_lazy("accounts:register")

    def get_object(self, queryset=None):

        login_user = self.request.user

        return get_object_or_404(
            Profile,
            username=self.kwargs.get('username'),
            user=login_user
        )
