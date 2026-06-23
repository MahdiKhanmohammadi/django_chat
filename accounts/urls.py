from django.urls import path
from .views import RegisterUserFormView, LoginUserFormView

app_name = "accounts"

urlpatterns = [
    path('register/', RegisterUserFormView.as_view(), name='register'),
    path('login/', LoginUserFormView.as_view(), name='login'),

]
