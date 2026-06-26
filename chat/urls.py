from django.urls import path
from .views import ProfileUpdateView, RoomListView, RoomDetailView
app_name = 'chat'

urlpatterns = [
    path('profile/<slug:username>/update/',
         ProfileUpdateView.as_view(), name='profile_update'),
    path('', RoomListView.as_view(), name="home"),
    path('room/<pk>/', RoomDetailView.as_view(), name="room"),
    # path("profile/<slug:username>/", name='user_profile'),

]
