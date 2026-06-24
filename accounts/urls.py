from django.urls import path
from .views import RegisterUserFormView, LoginUserFormView, logout_user

app_name = "accounts"

urlpatterns = [
    path('register/', RegisterUserFormView.as_view(), name='register'),
    path('login/', LoginUserFormView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

]
