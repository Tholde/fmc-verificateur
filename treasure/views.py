import datetime
import pandas as pd

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse

from treasure.models import User, Recap, Verification


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


def church_counts_by_mounth(request):
    dimes_by_church = Recap.objects.all().values('church').annotate(total_dimes=Sum('dimes')).order_by('church')
    return JsonResponse({'dimes_by_church': list(dimes_by_church)})


def dashboard(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        try:
            distinct_districts = Recap.objects.values('district').distinct()
            distinct_church = Recap.objects.values('church').distinct()
            total_dimes = Recap.objects.aggregate(total_dimes=Sum('dimes'))['total_dimes']
            recent_month = Recap.objects.annotate(month=TruncMonth('date')).latest('month').month
            total_dimes_recent_month = Recap.objects.filter(
                date__year=recent_month.year, date__month=recent_month.month
            ).aggregate(total_dimes=Sum('dimes'))['total_dimes']
            dimes_by_church = Recap.objects.all().values('church').annotate(total_dimes=Sum('dimes')).order_by('church')
            for dimes in dimes_by_church:
                print(dimes)
            for district in distinct_districts:
                print(district)
            for church in distinct_church:
                print(church)
            print(total_dimes)
            print(total_dimes_recent_month)
            context = {'user': user, 'distinct_districts': distinct_districts, 'distinct_church': distinct_church,
                       'dimes': total_dimes_recent_month, 'church_dimes': dimes_by_church}
            if user.role == 'secretary':
                return render(request, 'user/secretary/dashboard.html', context, status=200)
            elif user.role == 'verificateur':
                return render(request, 'user/verificateur/dashboard.html', context, status=200)
            else:
                return redirect('login')
        except Recap.DoesNotExist:
            distinct_districts = None
            total_dimes_recent_month = 0
            distinct_church = None
            context = {'user': user, 'distinct_districts': distinct_districts, 'distinct_church': distinct_church,
                       'dimes': total_dimes_recent_month}
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
        recap = Recap.objects.filter(is_verified=False).order_by('-created')
        search_query = request.GET.get('search', '')
        if user.role == 'secretary':
            if search_query:
                recap = recap.filter(number__in=int(search_query)) | recap.filter(
                    church__icontains=str(search_query).lower()) | recap.filter(
                    district__icontains=str(search_query).lower()) | recap.filter(
                    reference__icontains=str(search_query).lower()) | recap.filter(
                    ref__icontains=str(search_query).lower())
                context = {'user': user, 'recap': recap}
                return render(request, 'user/secretary/recap-list.html', context, status=200)
            context = {'user': user, 'recap': recap}
            return render(request, 'user/secretary/recap-list.html', context, status=200)
        elif user.role == 'verificateur':
            context = {'user': user, 'recap': recap}
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
        # try:
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
        # except:
        #     print('Something went wrong.')
        #     return redirect('dashboard')


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
                dimes = float(request.POST['dimes'])
                total = float(request.POST['total'])
                period = request.POST['period']
                reference = request.POST['reference']
                datereg = request.POST['datereg']
                montant = float(request.POST['montant'])
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
            try:
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
                    recap = Recap.objects.create(
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
                    recap.save()
                    Verification.objects.create(recap=recap)
                return redirect('manage_recap')
            except:
                messages = ('Essayer de definir l\'en tete de votre fichier comme number, date, church, district, '
                            'dimes, total, period, reference, datereg, montant et ref.')
                context = {'user': request.user, 'messages': messages}
                return render(request, 'user/secretary/echec_importation.html', context, status=404)
        return redirect('dashboard')


def export_recap_to_excel(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        user_id = request.session.get('user')
        user = User.objects.get(id=user_id)
        if user.role == 'secretary':
            recaps = Recap.objects.all().values('number', 'date', 'church', 'district',
                                                'dimes', 'total', 'period', 'reference',
                                                'datereg', 'montant', 'ref')
            df = pd.DataFrame(list(recaps))
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="recap_data.xlsx"'
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return response
        else:
            recaps = Recap.objects.all().values('number', 'date', 'church', 'district',
                                                'dimes', 'total', 'period', 'reference',
                                                'montant')
            df = pd.DataFrame(list(recaps))
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="recap_data.xlsx"'
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return response


# ***************************************** VERIFICATEUR *********************************
def manage_detail(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        user_id = request.session.get('user')
        user = User.objects.get(id=user_id)
        verification = Verification.objects.get(recap=id)
        context = {'user': user, 'verification': verification}
        if user.role == 'verificateur':
            return render(request, 'user/verificateur/verification.html', context, status=200)
        else:
            return redirect('dashboard')


def save_detail(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        user_id = request.session.get('user')
        user = User.objects.get(id=user_id)
        recap = get_object_or_404(Recap, id=id)
        verification = Verification.objects.get(recap=recap)
        try:
            if request.method == 'POST':
                # recap_number = request.POST.get('number')
                # recap = Recap.objects.get(number=recap_number)
                eds = request.POST.get('eds')
                prosperty = request.POST.get('prosperity')
                aniversary = request.POST.get('aniversary')
                worship = request.POST.get('worship')
                federation = request.POST.get('federation')
                mondial = request.POST.get('mondial')
                special = request.POST.get('special')
                frais = request.POST.get('frais')
                entree = request.POST.get('entree')
                sortie = request.POST.get('sortie')
                somme = float(eds) + float(aniversary) + float(prosperty) + float(worship) + float(federation) + float(
                    mondial) + float(special) + float(frais)
                if somme == recap.total:
                    print("Mety ny verification")
                    verification.eds = eds
                    verification.prosperity = prosperty
                    verification.aniversary = aniversary
                    verification.worship = worship
                    verification.federation = federation
                    verification.mondial = mondial
                    verification.special = special
                    verification.frais = frais
                    verification.entree = entree
                    verification.sortie = sortie
                    verification.save()
                    recap.is_verified = True
                    recap.save()
                    return redirect('manage_recap')
                else:
                    print("Misy diso ny kaonty")
                    messages = (
                        "Erreur de verificatio. Le total de votre verification n'est pas compatible au total grand "
                        "livre.")
                    context = {'user': user, 'messages': messages, 'verification': verification}
                    return render(request, 'user/verificateur/verification.html', context, status=404)
        except:
            messages = "Erreur d'enter."
            context = {'user': user, 'messages': messages, 'verification': verification}
            return render(request, 'user/verificateur/verification.html', context, status=404)


def logout(request):
    request.session.pop('user', None)
    request.session.modified = True
    return redirect('login')