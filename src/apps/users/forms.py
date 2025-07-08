from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("E-mailadres"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    first_name = forms.CharField(
        label=_("Voornaam"),
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'given-name'})
    )
    last_name = forms.CharField(
        label=_("Achternaam"),
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'family-name'})
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove username field since we use email
        if 'username' in self.fields:
            del self.fields['username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("E-mailadres"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'autofocus': True
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update the username field label since it's actually email
        self.fields['username'].label = _("E-mailadres")
        self.fields['password'].label = _("Wachtwoord")