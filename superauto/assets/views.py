#coding:utf-8
from django.shortcuts import render,render_to_response
from django import forms
from assets.models import Dept,AssetDetails,EmployeeUser
from superauto import settings
from django.views.generic import View, TemplateView, ListView, DetailView
from django.db.models import Q
from django.contrib import auth
from forms import Loginform
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.views.generic import View

# Create your views here.



def login(request):
    if request.method=='GET':
        form =Loginform()
        return render_to_response('login.html',RequestContext(request,{'form':form}))
    else:
        form = Loginform(request.POST)
        if form.is_valid():
            username=request.POST.get('username','')
            password=request.POST.get('password','')
            user=auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return render_to_response('index.html',{'username':username})
            else:
                return render_to_response('login.html',RequestContext(request,{'form':form,'password_is_wrong':True}))
        else:
            render_to_response('login.html',RequestContext(request,{'form':form}))


@login_required
def logout(request):
        auth.logout(request)
        return HttpResponseRedirect("login/")



class jiazai(View):
    def post(self, request, *args, **kwargs):
        # 获取当前用户
        user = self.request.user
        # 判断当前用户是否是活动的用户
        if not user.is_authenticated():
            return HttpResponseRedirect("login/")


class BaseMixin(object):

    def get_context_data(self, *args, **kwargs):


        context = super(BaseMixin, self).get_context_data(**kwargs)
        erros=[]

        try:
            # 网站标题等内容
            context['website_title'] = settings.WEBSITE_TITLE
            context['website_welcome'] = settings.WEBSITE_WELCOME

        except Exception as e:
            erros.append(u'加载基本信息出错')

        return context


class IndexView(BaseMixin, ListView):

    template_name = 'index.html'
    context_object_name = 'assetdetails_list'
    paginate_by = settings.PAGE_NUM  # 分页--每页的数目

    def get_queryset(self):

        assetdetails_list = AssetDetails.objects.filter(status=1)
        return assetdetails_list



class AssetDetailsView(BaseMixin, ListView):
    queryset = AssetDetails.objects.filter(Q(status=0) | Q(status=1))
    template_name = 'assetdetail.html'
    context_object_name = 'assetdetails_list'
    slug_field = 'id'

    def get_queryset(self):
        assetdetails_list = AssetDetails.objects.filter(
            status=0
        ).order_by("itno")[0:settings.PAGE_NUM]
        return assetdetails_list


class DeptView(BaseMixin,ListView):


    template_name = 'dept.html'
    context_object_name = 'dept_list'
    def get_context_data(self, **kwargs):
        kwargs['PAGE_NUM'] = settings.PAGE_NUM
        return super(DeptView, self).get_context_data(**kwargs)

    def get_queryset(self):
        dept_list = Dept.objects.all()[0:settings.PAGE_NUM]
        return dept_list

class EmployeeUserView(BaseMixin,ListView):
    template_name = 'user.html'
    context_object_name = 'user_list'
    def get_context_data(self, *args, **kwargs):
        kwargs['PAGE_NUM']=settings.PAGE_NUM
        return  super(EmployeeUserView,self).get_context_data(**kwargs)

    def get_queryset(self):
        user_list=EmployeeUser.objects.all()[0:settings.PAGE_NUM]
        return user_list