from django.shortcuts import render

def register_view(request):
    return render(request, "userauths/sign-up.html")