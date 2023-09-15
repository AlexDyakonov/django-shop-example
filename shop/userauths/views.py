from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User
from core.models import Product, Category, Cart, CartItem, Order

# User = settings.AUTH_USER_MODEL
categories = Category.objects.all()


def register_view(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)

        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"{username}, ваш аккаунт успешно создан.")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
                                    )
            login(request, new_user)
            return redirect("core:home")
        
    else:
        form = UserRegisterForm()    

    context = {
        'form': form,
        "categories" : categories,
    }

    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Вы уже вошли в аккаунт.")
        return redirect("core:home")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email = email, password = password)

            if user is not None:
                login(request, user)
                messages.success(request, "Вы уже вошли в аккаунт!")
                return redirect("core:home")
            else:
                messages.warning(request, "Данный пользователь не существует, зарегестрируйтесь.")
        except:
            messages.warning(request, f"Пользователя с почтой {email} не существует.")

    context = {
        "categories" : categories,
    }

    return render(request, "userauths/sign-in.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из аккаунта.")

    return redirect("userauths:sign-in")

def my_account(request):

    if request.user.is_authenticated:
        context = {
           "username" : request.user.username,
           "email" : request.user.email,
           "categories" : categories,
        }

        return render(request, "userauths/my-account.html", context)
    else:
        messages.warning(request, "Необходимо войти в аккаунт.")
        return redirect("core:home")