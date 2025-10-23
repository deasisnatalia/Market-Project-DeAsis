from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') #cambiar
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'