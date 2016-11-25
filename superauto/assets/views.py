#coding:utf-8
from django.shortcuts import render,render_to_response
from django import forms
from assets.models import Dept,AssetDetails,EmployeeUser,SiteInfo
from superauto import settings
from django.views.generic import View, TemplateView, ListView, DetailView
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.models import User
from forms import LoginForm
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,Http404
from django.views.generic import View
import superauto.settings
from django.views.generic import View
from assets.forms import AddDeptForm,ChangepwdForm,PasswordRestForm,SetPasswordForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import (base36_to_int, is_safe_url,
                               urlsafe_base64_decode, urlsafe_base64_encode)

from django.http import HttpResponse
# Create your views here.




@login_required
def index(request):
    username = request.user.username

    return render_to_response('index.html',{
            "title":u'主页',
            'username':username},context_instance = RequestContext(request))



@login_required
def syscolor(request):
    username = request.user.username
    return render_to_response('include/sys-colors.html', {'username': username})


@login_required
def updept(request):
    username = request.user.username
    return render_to_response('include/dept/updept.html', {'username': username})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")

@login_required
def changepwd(request):
    if request.method=='GET':
        form=ChangepwdForm()
        return render_to_response('registration/changepwd.html',RequestContext(request, {'form': form,}))
    else:
        form=ChangepwdForm(request.POST)
        if form.is_valid():
            username=request.user.username
            oldpwd=request.POST.get('oldpassword','')
            user=auth.authenticate(username=username,password=oldpwd)
            if user is not None and user.is_active:
                newpwd=request.POST.get('newpassword1','')
                user.set_password(newpwd)
                user.save()
                return render_to_response('index.html',RequestContext(request,{'changepwd_success':True}))
            else:
                return render_to_response('registration/changepwd.html',
                                          RequestContext(request, {'form': form, 'oldpassword_is_wrong': True}))
        else:
            return render_to_response('registration/changepwd.html', RequestContext(request, {'form': form, }))


def forgetpassword(request):
    if request.method=='GET':
        form=PasswordRestForm()
        return render_to_response('registration/forgot_password.html',RequestContext(request, {'form': form,}))
    else:
        form = PasswordRestForm(request.POST)

        if form.is_valid():
            token_generator = default_token_generator
            from_email = None
            opts = {
                'token_generator': token_generator,
                'from_email': from_email,
                'request': request,
            }
            user = form.save(**opts)
            return render_to_response('user_login.html', RequestContext(request, {'success':True }))
        else:
            return render_to_response('registration/forgot_password.html', RequestContext(request, {'form': form, }))


def resetpassword(request,uidb64,token):
    uidb64 = uidb64
    token = token
    if request.method=='GET':
        form=SetPasswordForm()
        return render_to_response('registration/resetpassword.html',RequestContext(request,{'form':form}))
    else:
        form=SetPasswordForm(request.POST)


        if form.is_valid():




            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User._default_manager.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            token_generator = default_token_generator

            if user is not None and token_generator.check_token(user, token):
                newpwd = request.POST.get('newpassword1', '')
                user.set_password(newpwd)
                user.save()

                return HttpResponse(u'修改成功哦！')



            else:
                return HttpResponse(
                    u"密码重设失败!\n密码重置链接无效，可能是因为它已使用。可以请求一次新的密码重置.",
                    status=403
                )
        else:
            return render_to_response('registration/resetpassword.html', RequestContext(request, {'form': form}))


"""
website_title=settings.WEBSITE_TITLE
WEBSITE_WELCOME=settings.WEBSITE_WELCOME

def login(request):
    if request.user.is_authenticated():
        return render_to_response('index.html',{'username':request.user.username})
    else:
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
        return HttpResponseRedirect("/login/")

@login_required
def IndexView(request):
    assetdetails_list = AssetDetails.objects.filter(status=1)
    username=request.user.username
    website_title=settings.WEBSITE_TITLE
    return render_to_response('index.html',locals())


def login(request):
    if request.user.is_authenticated():
        return render_to_response('index.html',{'username':request.user.username})
    else:
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
        return HttpResponseRedirect("/login/")


class BaseMixin(object):

    def denglu(self):
        user= self.request.user
        if user.is_authenticated():
            pass
        else:
            return HttpResponseRedirect('/login/')

    def get_context_data(self, *args, **kwargs):

        context = super(BaseMixin, self).get_context_data(**kwargs)
        erros=[]
        #username=self.request.user.username
        try:
            # 网站标题等内容
            context['website_title'] = settings.WEBSITE_TITLE
            context['website_welcome'] = settings.WEBSITE_WELCOME

            #context['username']=request.user.username
            #context['username']=username
            user = self.request.user
            if user.is_authenticated():
                context['username']=user.username

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


    template_name = 'dept/dept.html'
    context_object_name = 'dept_list'
    paginate_by = settings.PAGE_NUM
    def get_context_data(self, **kwargs):
        kwargs['PAGE_NUM'] = settings.PAGE_NUM
        return super(DeptView, self).get_context_data(**kwargs)

    def get_queryset(self):
        dept_list = Dept.objects.all()
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




def AddDeptView(request):
    if request.method == 'POST':
        form = AddDeptForm(request.POST)
        if form.is_valid():
            deptinfo = form.save()
            deptinfo.save()
            return HttpResponseRedirect('/dept/')
    else:
        form = AddDeptForm()
    return render(request, 'dept/adddept.html', {'deptform': form})

def EditDeptView(request):
    if request.method=='POST':
        form=AddDeptForm(request.POST)
        if form.is_valid():
            return render_to_response('dept/eritdept.html', {
                'form': form,}, context_instance = RequestContext(request))

        else:
            return render_to_response('dept/eritdept.html', {

                'form':form,
               }, context_instance = RequestContext(request))

"""