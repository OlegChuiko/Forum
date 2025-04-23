from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate
from django.shortcuts import render, redirect
from .forms import RegisterForm

def form(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index') 
    else:
        form = RegisterForm()
    
    return render(request, 'form/form.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'form/loginForm.html', {'form': form, 'error': 'Невірне ім\'я користувача або пароль.'})
    else:
        form = AuthenticationForm()
    return render(request, 'form/loginForm.html', {'form': form})