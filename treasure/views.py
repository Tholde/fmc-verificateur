from django.shortcuts import render


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


def why(request):
    return render(request, 'why.html')
