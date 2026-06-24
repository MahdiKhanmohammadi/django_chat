from django import forms
from accounts.models import Profile


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name',
                  'about', 'image_profile', 'banner']

        widgets = {
            'first_name': forms.widgets.TextInput(attrs={
                "class": "form-control", "id": "firstName",
                "placeholder": "Your Name"
            }),
            'last_name': forms.widgets.TextInput(attrs={
                "class": "form-control", "id": "lastName",
                "placeholder": "Your Last Name"
            }),
            'about': forms.widgets.Textarea(attrs={
                "class": "form-control"
            }),
            'image_profile': forms.widgets.FileInput(attrs={
                'class': 'form-control'
            }),
            'banner': forms.widgets.FileInput(attrs={
                'class': 'form-control'
            }),
        }
