from django.shortcuts import render
from django.views.generic import UpdateView, ListView, DetailView
from django.views.generic.detail import BaseDetailView
from .forms import ProfileModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.models import Profile
from .models import Room
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


class RoomListView(LoginRequiredMixin, ListView):
    template_name = "chat/index.html"
    context_object_name = 'rooms'

    def get_queryset(self):
        return Profile.objects.get(pk=self.request.user.pk).rooms.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for room in context["rooms"]:
            room.other_user = room.users.exclude(
                user=self.request.user
            ).first()

            room.last_message = room.messages.last()

        return context


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    context_object_name = 'room'
    template_name = "chat/room.html"

    def get_object(self):
        current_room_id = self.kwargs.get('pk')
        login_user = self.request.user
        return get_object_or_404(Room, pk=current_room_id,
                                 users__user=login_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # data for current chat room

        room = context.get('room')

        room.other_user = room.users.exclude(
            user=self.request.user).first()

        room.messages.order_by("-send_date").all()

        # room.other_user_messages = room.other_user.messages.filter(
        #     room__pk=room.pk).all()

        # room.login_user_messages = Profile.objects.filter(
        #     user=self.request.user).first().messages.filter(room__pk=self.kwargs['pk']).all()

        context['room'] = room

        # data for sidebar
        context['rooms'] = Profile.objects.get(
            pk=self.request.user.pk).rooms.all()

        for room in context["rooms"]:
            room.other_user = room.users.exclude(
                user=self.request.user
            ).first()

        return context
