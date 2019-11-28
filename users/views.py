from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User

# Create your views here.


def logout_view(request):
    """用户注销后重定向到index视图"""
    logout(request)
    return HttpResponseRedirect(reverse('dw_query:index'))


def _allowed_register(name):
    """if new_user.name is in <User.username> then allowed to register"""
    users = User.objects.all()
    allowed_names = {user.user_name for user in users}
    return name in allowed_names


def register(request):
    """用户注册"""
    if request.method != 'POST':
        form = UserCreationForm()
        msg = ''
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid() and _allowed_register(request.POST['username']):
            new_user = form.save()
            auth_user = authenticate(username=new_user.username,
                                     password=request.POST['password1'])
            login(request, auth_user)
            return HttpResponseRedirect(reverse('dw_query:index'))
        else:
            msg = '不能注册用户名"{}", 请向管理员索取账号.'.format(request.POST['username'])
    context = {'form': form, 'msg': msg}
    return render(request, 'users/register.html', context)


def audit_help(request):
    return render(request, 'users/howtoaudit.html')
