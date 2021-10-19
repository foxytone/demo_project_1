from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.views import LoginView


# Create your views here.


def registration(request: HttpRequest) -> HttpResponse:
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # messages.success(request, 'Registration completed successfully')
            return redirect('/tasks/')
    return render(request, 'registration/registration.html', {'form': form})


def login_(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        return LoginView.as_view()(request)
