import datetime
import pandas as pd

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect

from treasure.models import User, Recap


def index(request):
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
        if user.role == 'secretary':
            return render(request, 'user/secretary/dashboard.html', context, status=200)
        elif user.role == 'verificateur':
            return render(request, 'user/verificateur/dashboard.html', context, status=200)
        else:
            return redirect('login')


def user_profile(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        context = {'user': user}
        if user.role == 'secretary':
            return render(request, 'user/secretary/profile.html', context, status=200)
        elif user.role == 'verificateur':
            return render(request, 'user/verificateur/profile.html', context, status=200)
        else:
            return redirect('dashboard')


def update_profile(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        try:
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
                                return render(request, 'user/secretary/profile.html', context, status=200)
                            elif user.role == 'verificateur':
                                return render(request, 'user/verificateur/profile.html', context, status=200)
                            else:
                                return redirect('dashboard')
                else:
                    user.fullname = fullname
                    user.email = email
                    user.contact = contact
                    user.save()
                    return redirect('dashboard')
        except:
            messages = 'Something went wrong.'
            context = {'user': user, 'messages': messages}
            if user.role == 'secretary':
                return render(request, 'user/secretary/profile.html', context, status=200)
            elif user.role == 'verificateur':
                return render(request, 'user/verificateur/profile.html', context, status=200)
            else:
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
                return render(request, 'user/secretary/profile.html', context, status=200)
            elif user.role == 'verificateur':
                return render(request, 'user/verificateur/profile.html', context, status=200)
            else:
                return redirect('dashboard')


def manage_recap(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        recap = Recap.objects.all().order_by('-created')
        context = {'user': user, 'recap': recap}
        if user.role == 'secretary':
            return render(request, 'user/secretary/recap-list.html', context, status=200)
        elif user.role == 'verificateur':
            return render(request, 'user/verificateur/report-list.html', context, status=200)
        else:
            return redirect('dashboard')


def recap_show(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        user_id = request.session.get('user')
        user = User.objects.get(id=user_id)
        recap = Recap.objects.get(id=id)
        context = {'user': user, 'recap': recap}
        return render(request, 'user/secretary/edit_recap.html', context, status=200)


def delete_recap(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        try:
            recap = Recap.objects.get(id=id)
            recap.delete()
            return redirect('manage_recap')
        except Recap.DoesNotExist:
            print('Recap does not exist')
            return redirect('dashboard')


def add_new_report(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        try:
            if request.method == 'POST':
                number = request.POST['number']
                date = request.POST['date']
                church = request.POST['church']
                district = request.POST['district']
                dimes = request.POST['dimes']
                total = request.POST['total']
                period = request.POST['period']
                reference = request.POST['reference']
                datereg = request.POST['datereg']
                montant = request.POST['montant']
                ref = request.POST['ref']
                recap = Recap(number=number, date=date, church=church, district=district, dimes=dimes, total=total,
                              period=period, reference=reference, datereg=datereg, montant=montant, ref=ref)
                recap.save()
                return redirect('add_new_report')
        except:
            print('Something went wrong.')
            return redirect('dashboard')


def update_recap(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        user_id = request.session.get('user')
        user = User.objects.get(id=user_id)
        try:
            recap = Recap.objects.get(id=id)
            if request.method == 'POST':
                number = request.POST['number']
                date = request.POST['date']
                church = request.POST['church']
                district = request.POST['district']
                dimes = request.POST['dimes']
                total = request.POST['total']
                period = request.POST['period']
                reference = request.POST['reference']
                datereg = request.POST['datereg']
                montant = request.POST['montant']
                ref = request.POST['ref']
                if recap:
                    recap.number = number
                    recap.date = date
                    recap.church = church
                    recap.district = district
                    recap.dimes = dimes
                    recap.total = total
                    recap.period = period
                    recap.reference = reference
                    recap.datereg = datereg
                    recap.montant = montant
                    recap.ref = ref
                    recap.save()
                    return redirect('manage_recap')
                else:
                    messages = 'Something went wrong.'
                    context = {'user': user, 'messages': messages}
                    if user.role == 'secretary':
                        return render(request, 'user/secretary/edit_recap.html', context, status=200)
        except:
            print('Something went wrong.')
            return redirect('dashboard')


def upload_excel(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        if request.method == 'POST':
            excel_file = request.FILES['excel']
            print("madalo eto\n")
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                print("mandalo eto\n")
                print(row)
                date = pd.to_datetime(row['date'], errors='coerce')
                period = pd.to_datetime(row['period'], errors='coerce')
                datereg = pd.to_datetime(row['datereg'], errors='coerce')

                if pd.isna(date) or pd.isna(period) or pd.isna(datereg):
                    print(f"Skipping row {index} due to invalid date(s)")
                    continue

                date = date.date()
                period = period.date()
                datereg = datereg.date()
                number = row['number'] if pd.notna(row['number']) else None
                church = row['church'] if pd.notna(row['church']) else ''
                district = row['district'] if pd.notna(row['district']) else ''
                dimes = row['dimes'] if pd.notna(row['dimes']) else 0
                total = row['total'] if pd.notna(row['total']) else 0
                reference = row['reference'] if pd.notna(row['reference']) else ''
                montant = row['montant'] if pd.notna(row['montant']) else 0
                ref = row['ref'] if pd.notna(row['ref']) else ''

                Recap.objects.create(
                    number=number,
                    date=date,
                    church=church,
                    district=district,
                    dimes=dimes,
                    total=total,
                    period=period,
                    reference=reference,
                    datereg=datereg,
                    montant=montant,
                    ref=ref
                )
            return redirect('manage_recap')
        return redirect('dashboard')


def export_recap_to_excel(request):
    recaps = Recap.objects.all().values('number', 'date', 'church', 'district',
                                        'dimes', 'total', 'period', 'reference',
                                        'datereg', 'montant', 'ref')
    df = pd.DataFrame(list(recaps))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="recap_data.xlsx"'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response


# ***************************************** VERIFICATEUR *********************************
def manage_detail(request,id):
    pass