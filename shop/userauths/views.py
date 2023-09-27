from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from userauths.models import User
from core.models import Category
from email_utils.email_utils import send_registration_email
from email_utils.email_utils import send_password_change_mail
from django.utils.translation import gettext as _
from django.utils.translation import get_language


messages = {
    'en': {
        'mail_exist': "A user with this email already exists.",
        'username_exist': "A user with this username already exists.",
        'password_mismatch': "Passwords do not match.",
        'account_created': "Your account has been successfully created, {username}.",
        'already_logged_in': "You are already logged in.",
        'user_does_not_exist': "This user does not exist, please register.",
        'user_email_does_not_exist': "User with email {email} does not exist.",
        'logged_out': "You have successfully logged out.",
        'password_changed': "Password successfully changed.",
        'incorrect_current_password': "Incorrect current password.",
        'logged_in' : 'Logged in!',
        "need_log_in": "Log in before action.",
    },
    'ru': {
        'mail_exist': "Пользователь с такой почтой уже существует.",
        'username_exist': "Пользователь с таким никнеймом уже существует.",
        'password_mismatch': "Пароли не совпадают.",
        'account_created': "Аккаунт успешно создан, {username}.",
        'already_logged_in': "Вы уже вошли в аккаунт.",
        'user_does_not_exist': "Данный пользователь не существует, зарегистрируйтесь.",
        'user_email_does_not_exist': "Пользователя с почтой {email} не существует.",
        'logged_out': "Вы успешно вышли из аккаунта.",
        'password_changed': "Пароль успешно изменен.",
        'incorrect_current_password': "Неправильно введен текущий пароль.",
        'logged_in' : 'Вы успешно вошли!',
        "need_log_in": "Необходимо войти в аккаунт.",
    },
}

def get_message(msg_id):
    current_language = get_language()
    if current_language in messages:
        if msg_id in messages[current_language]:
            return messages[current_language][msg_id]
    
    return "None"


# User = settings.AUTH_USER_MODEL
categories = Category.objects.all()

def register_view(request):
    context = {
        "categories" : categories,
    }

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            context["msz"] = get_message('password_mismatch')
            context["col"] = "alert-danger"
        else:
            if User.objects.filter(username=username).exists():
                context["msz"] = get_message('username_exist')
                context["col"] = "alert-danger"
            elif User.objects.filter(email=email).exists():
                context["msz"] = get_message('mail_exist')
                context["col"] = "alert-danger"
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                messages.success(request, get_message('account_created').format(username=username))
                new_user = authenticate(username=email,
                                        password=password1
                                        )
                login(request, new_user)
                user = request.user
                send_registration_email(user=user)
                return redirect("core:home")

    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, get_message('already_logged_in'))
        return redirect("core:home")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email = email, password = password)

            if user is not None:
                login(request, user)
                messages.success(request, get_message('logged_in'))
                return redirect("core:home")
            else:
                messages.warning(request, get_message('user_does_not_exist'))
        except:
            messages.warning(request, get_message('user_email_does_not_exist').format(email=email))

    context = {
        "categories" : categories,
    }

    return render(request, "userauths/sign-in.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, get_message('logged_out'))

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
                context["msz"] = get_message('password_changed')
                user = User.objects.get(username=username)
                login(request,user)
                send_password_change_mail(user)
            else:
                context["msz"] = get_message('incorrect_current_password')
                context["col"] = "alert-danger"

            return render(request, "userauths/my-account.html", context)
        return render(request, "userauths/my-account.html", context)
    else:
        messages.warning(request, get_message('need_log_in'))
        return redirect("core:home")