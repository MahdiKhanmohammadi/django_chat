from django.urls import path
from .views import ProfileUpdateView
app_name = 'chat'

urlpatterns = [
    path('profile/<slug:username>/update/',
         ProfileUpdateView.as_view(), name='profile_update')

]
