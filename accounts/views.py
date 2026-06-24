from django.shortcuts import render
from django.views.generic import FormView
from .forms import RegisterUserModelForm, LoginUserForm
from .models import User
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.shortcuts import redirect
# Create your views here.


class RegisterUserFormView(FormView):
    form_class = RegisterUserModelForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form: RegisterUserModelForm):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        create_user = User.objects.create(email=email)
        create_user.set_password(password)
        create_user.save()

        return super().form_valid(form)


class LoginUserFormView(FormView):
    form_class = LoginUserForm
    template_name = "accounts/login.html"

    def form_valid(self, form: LoginUserForm):

        get_email = form.cleaned_data.get('email')
        get_password = form.cleaned_data.get('password')

        user = authenticate(self.request, username=get_email,
                            password=get_password)

        if not user:
            form.add_error('email', "email or password wrong")
            return self.form_invalid(form)

        login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("chat:profile_update", kwargs={'username': self.request.user.generate_username()})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("accounts:login")
