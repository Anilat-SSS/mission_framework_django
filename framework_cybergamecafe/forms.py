from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas !")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # 🔥 HASH PASSWORD

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    pass