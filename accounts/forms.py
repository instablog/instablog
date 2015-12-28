import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    def clean_password2(self):
        password2 = super(SignupForm, self).clean_password2()
        if password2:
            if len(password2) < 4:
                raise forms.ValidationError('more than 4')
            elif re.match(r'^\d+$', password2):
                raise forms.ValidationError("Don't use only numbers")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Already exists.')
        return email

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class QuizLoginForm(AuthenticationForm):
    answer = forms.CharField(help_text='3+3=?')

    def clean_answer(self):
        answer = self.cleaned_data.get('answer', '').strip()
        if answer:
            if answer != '6':
                raise forms.ValidationError('Wrong.')
        return answer


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('biography',)
