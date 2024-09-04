from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from treasure.models import User


# Create your views here.
def index(request):
    # from django.http import JsonResponse
    # return JsonResponse({"message": "Hello World"})
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def service(request):
    return render(request, 'service.html')


def team(request):
    return render(request, 'team.html')


def login(request):
    return render(request, 'auth/auth-login.html')


def register_page(request):
    return render(request, 'auth/auth-register.html')


def save_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        fullname = request.POST['fullname']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']
        if len(password) > 7:
            if password == confirm_password:
                if len(request.FILES) != 0:
                    pwd = make_password(password)
                    image = request.FILES['image']
                    user = User(email=email, fullname=fullname, password=pwd,
                                role=role, image=image)
                    user.save()
                    messages = 'Your account has been created.'
                    context = {'user': user, 'messages': messages}
                    return render(request, 'auth/auth-login.html', context, status=200)
                else:
                    messages = 'Sorry, you have not entered the image.'
                    return render(request, 'auth/auth-register.html', {'messages': messages}, status=404)
            else:
                messages = 'Sorry, verify your password and confirm it again.'
                return render(request, 'auth/auth-register.html', {'messages': messages}, status=500)

        else:
            messages = 'Sorry, your password is very short. Try again and do it 8 character long.'
            return render(request, 'auth/auth-register.html', {'messages': messages}, status=400)

def connexion(request):
    return render(request, 'auth/auth-login.html')
def dashboard(request):
    return render(request, 'secretaire/dashboard.html')