from django import forms
from .models import User


class RegisterUserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        max_length=100, widget=forms.widgets.PasswordInput(attrs={
            'class': "form-control", "id": "repeat-password", 'placeholder': "password again"
        }))

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

        widgets = {
            'email': forms.widgets.EmailInput(attrs={'class': "form-control", 'id': "email-address", 'placeholder': "youremail@example.com"}),

            'password': forms.widgets.PasswordInput(attrs={
                'class': "form-control", "id": "password", 'placeholder': "password"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            self.add_error("password",
                           "password and confirm password not match")

        return cleaned_data


class LoginUserForm(forms.Form):
    email = forms.EmailField(widget=forms.widgets.EmailInput(attrs={
        'class': "form-control", "id": "email-address",
        "placeholder": "youremail@example.com"
    }))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={
        'class': "form-control", 'id': "password", "placeholder": "password"
    }))
