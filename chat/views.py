from django.views.generic import UpdateView, ListView, DetailView
from .forms import ProfileModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Profile
from .models import Room
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Count

# Create your views here.


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileModelForm
    template_name = "chat/profile_update.html"
    model = Profile
    slug_field = 'username'
    slug_url_kwarg = 'username'
    success_url = reverse_lazy("chat:home")

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
        rooms = Profile.objects.get(pk=self.request.user.pk).rooms.all()
        return rooms.annotate(
            message_count=Count('messages')).filter(message_count__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for room in context["rooms"]:
            room.other_user = room.users.exclude(
                user=self.request.user
            ).first()

            room.last_message = room.messages.first()
            room.display_last_message_send_date = room.last_message.display_message_date

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

        context['room'] = room

        # data for sidebar
        context['rooms'] = Profile.objects.get(
            # 'books' is the related_name in Book model's ForeignKey
            pk=self.request.user.pk).rooms

        context['rooms'] = context['rooms'].annotate(
            message_count=Count('messages')).filter(message_count__gt=0)

        for room in context["rooms"]:
            room.other_user = room.users.exclude(
                user=self.request.user
            ).first()

            # show display date in rooms
            room.display_last_message_send_date = room.messages.first().display_message_date

        return context


class ContactListView(LoginRequiredMixin, ListView):
    pass
