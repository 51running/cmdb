from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from .models import Host

def index(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    results = [host.as_dict() for host in Host.objects.all()]
    return render(request,'asset/index.html',{
        'results':results
    })

def list_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code': 403})
    result = [host.as_dict() for host in Host.objects.all()]
    return JsonResponse({'code':200,'result':result})

