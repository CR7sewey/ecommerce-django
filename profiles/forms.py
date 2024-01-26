# to register
# to update
from django import forms
from django.core.exceptions import ValidationError
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class ProfileForm(forms.ModelForm):  # validacoes ja feitas no models!
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ('user',)


class UserForm(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs):  # if user already logged in
        super().__init__(*args, **kwargs)
        self.user = user

    # SIMILAR TO MODELS
    first_name = forms.CharField(
        widget=forms.TextInput(),
        label='First Name',
        required=True
    )

    last_name = forms.CharField(
        widget=forms.TextInput(),
        label='Last Name',
        required=False
    )

    email = forms.EmailField(
        widget=forms.EmailInput(),
        label='Email',
        required=True
    )

    username = forms.CharField(
        widget=forms.TextInput(),
        label='Username',
        required=True
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password',
        required=False
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password confirmation',
        required=False
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email',
                  'username', 'password1', 'password2')

    def clean(self, *args, **kwargs):
        # o que vem do forms!
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        user_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password1')
        password2_data = cleaned.get('password2')

        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'User already exists'
        error_msg_email_exists = 'E-mail already exists'
        error_msg_password_match = 'The two passwords doesn\'t match!'
        error_msg_password_short = 'The password needs at least 6 characters'

        # Usuários logados: atualização
        if self.user:
            if user_db:
                if user_data != user_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password1'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                if len(password_data) < 6:
                    validation_error_msgs['password1'] = error_msg_password_short

        # Usuários não logados: cadastro
        else:
            validation_error_msgs['username'] = error_msg_user_exists

        if validation_error_msgs:
            raise (ValidationError(validation_error_msgs))
