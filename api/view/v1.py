#encoding:utf-8
import json
from django.views.generic import View
from django.http import JsonResponse,HttpResponse
from asset.models import Host,Resource
from django.views.decorators.csrf import csrf_exempt

class APIView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(APIView,self).dispatch(request,*args,**kwargs)

    def get_json(self):
        try:
            return json.loads(self.request.body)
        except BaseException as e:
            return {}

    def response(self,result=None,code=200,error={}):
        return JsonResponse({'code':code,'result':result,'error':error})

class ClinetView(APIView):

    def get(self,request,*args,**kwargs):
        print(request.body)
        return HttpResponse("get request")

    def post(self,request,*args,**kwargs):
        # print(kwargs.get("ip", ""))
        _ip = kwargs.get("ip","")
        _json = self.get_json()
        host = Host.create_or_replace(_ip,_json.get('name',''),_json.get('mac',''),_json.get('os',''),_json.get('arch',''),_json.get('mem',0),_json.get('cpu',0),_json.get('disk',{}))

        return self.response(host.as_dict())

class ResourceView(APIView):
    def post(self,request,*args,**kwargs):
        _ip = kwargs.get("ip","")
        _json = self.get_json()

        Resource.create_obj(_ip,_json.get('cpu'),_json.get('mem'))
        return self.response()