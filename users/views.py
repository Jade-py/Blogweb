from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, RegistrationForm, LoginForm
from .models import UserProfile, CustomUser
from django.urls import reverse_lazy
from django.shortcuts import render,  redirect
from datetime import datetime


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']

            user = form.save()  # Save the user object

            # Authenticate and log in the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('registration'))
            else:
                print("Authentication failed")
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'Signup.html', {'form': form})


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper


@login_required
def registration_view(request):
    current_year = datetime.now().year
    year_range = range(current_year, current_year + 7)
    context = {
        'year_range': year_range
    }

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            profile = UserProfile(user=request.user,
                                  first_name=form.cleaned_data['first_name'],
                                  last_name=form.cleaned_data['last_name'],
                                  college_name=form.cleaned_data['college_name'],
                                  stream=form.cleaned_data['stream'],
                                  graduation_year=form.cleaned_data['graduation_year'],
                                  phone_no=form.cleaned_data['phone_no']
                                  )
            profile.save()
            return redirect(reverse_lazy('workspace'))
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


class LoginView(LoginView):
    form_class = LoginForm

    def login_view(request):
        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                pass
            else:
                return render(request, 'login.html', {'form': form})
        else:
            form = LoginForm()
            return render(request, 'login.html', {'form': form})


def home_view(request):
    return render(request, 'home.html')