from django.views.generic import UpdateView, ListView, DetailView, View
from django.views.decorators.csrf import csrf_exempt
from .forms import ProfileModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Profile
from .models import Contact, Room
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.db.models import Count
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator

# Create your views here.


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileModelForm
    template_name = "chat/profile_update.html"
    model = Profile
    success_url = reverse_lazy("chat:home")

    def get_object(self, queryset=None):

        login_user = self.request.user

        return get_object_or_404(
            Profile,
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
    model = Contact
    context_object_name = 'contacts'
    template_name = "chat/contact.html"

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user.profile)


class GetOrCreateRoomView(LoginRequiredMixin, View):
    def get(self, request, contact_username):
        find_contact = get_object_or_404(Profile, username=contact_username)
        login_user = request.user.profile

        get_exist_room = Room.objects.filter(
            users=login_user).filter(users=find_contact).first()

        if get_exist_room == None:
            room = Room.objects.create()
            room.users.add(find_contact, login_user)
            return redirect(reverse_lazy("chat:room", kwargs={'pk': room.pk}))

        return redirect(reverse_lazy("chat:room", kwargs={'pk': get_exist_room.pk}))


@method_decorator(csrf_exempt, name='dispatch')
class ProfileListView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "chat/find_contact.html")

    def post(self, request, ):
        query = request.POST.get('query')
        contacts = []
        profiles = Profile.objects.filter(username__contains=query)
        for profile in profiles:
            contacts.append({
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "username": profile.username,
                "image_profile": profile.image_profile.url if profile.image_profile else "",
            })

        if contacts:
            return JsonResponse({"contacts": contacts})
        return JsonResponse({"detail": "user notfound"})


@method_decorator(csrf_exempt, name='dispatch')
class AddContactView(LoginRequiredMixin, View):
    def post(self, request):
        current_user = request.user.profile

        username = request.POST.get('username')
        contact_user = get_object_or_404(Profile, username=username)

        check_contact_exist = Contact.objects.filter(
            owner=current_user, contact_user=contact_user).exists()
        if check_contact_exist:
            return JsonResponse({'detail': False})

        Contact.objects.create(owner=current_user, contact_user=contact_user)
        return JsonResponse({'detail': True})


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = "chat/profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user_profile = self.request.user.profile
        context['contacts'] = current_user_profile.contacts.all()
        return context
