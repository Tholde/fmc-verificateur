from django.shortcuts import render


# Create your views here.
def index(request):
    # from django.http import JsonResponse
    # return JsonResponse({"message": "Hello World"})
    return render(request, 'home/index.html')
