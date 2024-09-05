import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect

from treasure.models import User, Recap


# Create your views here.
def index(request):
    # from django.http import JsonResponse
    # return JsonResponse({"message": "Hello World"})
    if request.session.get('user'):
        return redirect('dashboard')
    else:
        return render(request, 'index.html')


def about(request):
    if request.session.get('user'):
        return redirect('dashboard')
    else:
        return render(request, 'about.html')


def service(request):
    if request.session.get('user'):
        return redirect('dashboard')
    else:
        return render(request, 'service.html')


def team(request):
    if request.session.get('user'):
        return redirect('dashboard')
    else:
        return render(request, 'team.html')


def login(request):
    if request.session.get('user'):
        return redirect('dashboard')
    else:
        return render(request, 'auth/auth-login.html')


def register_page(request):
    if request.session.get('user'):
        return redirect('dashboard')
    else:
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
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email).first()
        if user:
            pwd = check_password(password, user.password)
            if pwd:
                request.session['user'] = user.id
                print('user is authenticated : ' + str(user.fullname))
                return redirect('dashboard')
            else:
                messages = 'Password is incorrect.'
                context = {'messages': messages}
                return render(request, 'auth/auth-login.html', context, status=404)

        else:
            messages = 'E-mail is incorrect.'
            context = {'messages': messages}
            return render(request, 'auth/auth-login.html', context, status=404)


def dashboard(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        context = {'user': user}
        return render(request, 'user/dashboard.html', context, status=200)


def user_profile(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        context = {'user': user}
        if user.role == 'secretary':
            return render(request, 'user/profile.html', context, status=200)


def update_profile(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        if request.method == 'POST':
            fullname = request.POST['fullname']
            email = request.POST['email']
            contact = request.POST['contact']
            password = request.POST['password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_new_password']
            if not password and not new_password and not confirm_password:
                pwd = check_password(password, user.password)
                if pwd:
                    if new_password == confirm_password:
                        new_pwd = make_password(new_password)
                        user.fullname = fullname
                        user.email = email
                        user.contact = contact
                        user.password = new_pwd
                        user.updated = datetime.timezone
                        user.save()
                        return redirect('dashboard')
                    else:
                        messages = 'New Password went wrong.'
                        context = {'user': user, 'messages': messages}
                        if user.role == 'secretary':
                            return render(request, 'user/profile.html', context, status=200)
            else:
                user.fullname = fullname
                user.email = email
                user.contact = contact
                user.save()
                return redirect('dashboard')


def update_image(request):
    if not request.session.get('user'):
        return redirect('login')
    if request.method == "POST":
        id = request.session.get('user')
        user = User.objects.get(id=id)
        if len(request.FILES) != 0:
            image = request.FILES['image']
            user.image = image
            user.updated = datetime.timezone
            user.save()
            return redirect('dashboard')
        else:
            messages = 'Something went wrong.'
            context = {'user': user, 'messages': messages}
            if user.role == 'secretary':
                return render(request, 'user/profile.html', context, status=200)
            else:
                return redirect('dashboard')


def manage_recap(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        recap = Recap.objects.all().order_by('-created')
        context = {'user': user, recap: recap}
        return render(request, 'user/recap-list.html', context, status=200)


def recap_show(request,id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        user_id = request.session.get('user')
        user = User.objects.get(id=user_id)
        context = {'user': user}
        return render(request, 'user/edit_recap.html', context, status=200)


def delete_recap(request):
    pass


def add_new_report(request):
    pass


def update_recap(request):
    pass
