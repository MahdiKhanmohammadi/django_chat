from django.urls import path
from .views import ProfileUpdateView, RoomListView, RoomDetailView, ContactListView, GetOrCreateRoomView, ProfileListView, AddContactView
from django.views.generic import TemplateView

app_name = 'chat'

urlpatterns = [
    path('profile/update/',
         ProfileUpdateView.as_view(), name='profile_update'),
    path('', RoomListView.as_view(), name="home"),
    path('room/<pk>/', RoomDetailView.as_view(), name="room"),
    path('contacts/', ContactListView.as_view(), name="contacts"),
    path('profile/<slug:contact_username>/get-room/',
         GetOrCreateRoomView.as_view(), name="get_room"),
    path("contacts/find/", ProfileListView.as_view()),
    path("contacts/add/", AddContactView.as_view()),

    # path("profile/<slug:username>/", name='user_profile'),

]
