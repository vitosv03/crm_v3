from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class LoginUserForm(AuthenticationForm):
    """
    remake fields in user login form
    """

    username = forms.CharField(label='Login', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    # def confirm_login_allowed(self, user):
    #     """
    #     Controls whether the given User may log in. This is a policy setting,
    #     independent of end-user authentication. This default behavior is to
    #     allow login by active users, and reject login by inactive users.
    #
    #     If the given user cannot log in, this method should raise a
    #     ``ValidationError``.
    #
    #     If the given user may log in, this method should return None.
    #     """
    #     if not user.is_active:
    #         raise self.ValidationError(
    #             self.error_messages['inactive'],
    #             code='inactive',
    #         )
    # def get_invalid_login_error(self):

        # User = get_user_model()
        #
        # user = User.objects.get(username=self.cleaned_data.get('username'))
        # print(user.exists())
        # # if not user.is_active and user:
        # #     raise forms.ValidationError(
        # #         self.error_messages['inactive'],
        # #         code='inactive', )
        # # else:
        # #     return forms.ValidationError(
        # #         self.error_messages['invalid_login'],
        # #         code='invalid_login',
        # #         # params={'username': self.username_field.verbose_name},
        # #     )


class UserRegisterForm(UserCreationForm):
    """
    remake fields in user registered form
    """
    email = forms.EmailField(required=True)

    class Meta:
        User = get_user_model()
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        group_users = Group.objects.get(name='Users')
        group_users.user_set.add(user)
        return user
