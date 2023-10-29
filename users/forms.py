from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from.models import CustomUser, UserProfile


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        error_messages = {
            'username': {'unique': 'User with this username already exists'},
            'email': {'unique': 'User with this email already exists'}
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your Password'})
        }
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)


class RegistrationForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        exclude = ['first_login', 'user']
        fields = ('first_name', 'last_name', 'college_name', 'stream', 'graduation_year', 'phone_no', 'first_login',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your First Name', 'width': '400px', 'height': '50px'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Last Name', 'width': '400px', 'height': '50px'}),
            'college_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter Your College Name', 'width': '400px',
                       'height': '50px'}),
            'stream': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter Your Stream', 'width': '400px',
                       'height': '50px'}),
            'graduation_year': forms.NumberInput(
                attrs={'class': 'form-control year-picker', 'placeholder': 'Enter Your Graduation Year', 'width': '400px',
                       'height': '50px'}),
            'phone_no': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter Your Phone Number', 'width': '400px',
                       'height': '50px'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].initial = None


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Username', 'width': '90%'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Password', 'width': '90%'})
        self.error_messages['invalid_login']="Username and Password didn't match"
