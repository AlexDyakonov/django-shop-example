from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL


def register_view(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)

        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Hey {username}, your account was created successfully.")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
                                    )
            login(request, new_user)
            return redirect("core:home")
        
    else:
        form = UserRegisterForm()    
    
    context = {
        'form': form,
    }

    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already logged in.")
        return redirect("core:home")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request, f"User with {email} does not exist.")

        user = authenticate(request, email = email, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in!")
            return redirect("core:home")
        else:
            messages.warning(request, "User does not exist, create an account.")

    context = {

    }

    return render(request, "userauths/sign-in.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out.")

    return redirect("userauths:sign-in")

def my_account(request):

    if request.user.is_authenticated:
        context = {
           "username" : request.user.username,
           "email" : request.user.email,
        }

        return render(request, "userauths/my-account.html", context)
    else:
        messages.warning(request, "Необходимо войти в аккаунт.")
        return redirect("core:home")