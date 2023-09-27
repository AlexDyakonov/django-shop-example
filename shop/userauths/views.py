from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from userauths.models import User
from core.models import Category
from email_utils.email_utils import send_registration_email
from email_utils.email_utils import send_password_change_mail
from django.utils.translation import gettext as _

# User = settings.AUTH_USER_MODEL
categories = Category.objects.all()

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)

        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, _(f"{username}, ваш аккаунт успешно создан."))
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
                                    )
            login(request, new_user)

            user = request.user
            send_registration_email(user=user)
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
        messages.warning(request, _("Вы уже вошли в аккаунт."))
        return redirect("core:home")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email = email, password = password)

            if user is not None:
                login(request, user)
                messages.success(request, _("Вы вошли в аккаунт!"))
                return redirect("core:home")
            else:
                messages.warning(request, _( "Данный пользователь не существует, зарегестрируйтесь."))
        except:
            messages.warning(request, _(f"Пользователя с почтой {email} не существует."))

    context = {
        "categories" : categories,
    }

    return render(request, "userauths/sign-in.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, _("Вы успешно вышли из аккаунта."))

    return redirect("userauths:sign-in")

def my_account(request):
    context = {
           "username" : request.user.username,
           "email" : request.user.email,
           "categories" : categories,
    }

    if request.user.is_authenticated:
        if request.method=="POST":
            current = request.POST["cpwd"]
            new_pas = request.POST["npwd"]

            user = User.objects.get(id=request.user.id)
            username = user.username

            check = user.check_password(current)

            if check==True:
                user.set_password(new_pas)
                user.save()
                context["msz"] = _("Пароль успешно изменен")
                user = User.objects.get(username=username)
                login(request,user)
                send_password_change_mail(user)
            else:
                context["msz"] = _("Текущий пароль введен неправильно")
                context["col"] = "alert-danger"

            return render(request, "userauths/my-account.html", context)
        return render(request, "userauths/my-account.html", context)
    else:
        messages.warning(request, _("Необходимо войти в аккаунт."))
        return redirect("core:home")