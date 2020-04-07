# _*_encoding:utf-8_*_
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from mysite import models, forms
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail

def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
        try:
            user = User.objects.get(username=username)
            diaries = models.Diary.objects.filter(user=user).order_by('-ddate')
        except:
            pass
    messages.get_messages(request)
    return render(request, 'index.html', locals())


def listing(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = models.Mood.objects.all()
    return render(request, 'listing.html', locals())

@login_required(login_url='/login/')
def posting(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)
    
    if request.method == 'POST':
        user = User.objects.get(username=username)
        diary = models.Diary(user=user)
        post_form = forms.DiaryForm(request.POST, instance=diary)
        if post_form.is_valid():
            messages.add_message(request, messages.INFO, '日记已存储')
            post_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, message.INFO, '如果要张贴日记，每一个选项都要填......')
    else:
        post_form = forms.DiaryForm()
        messages.add_message(request, messages.INFO, '如果要张贴日记，每一个字段都要填......')
    return render(request, 'posting.html', locals())
        
        
def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message='感谢你的来信'
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']
        else:
            message='请检查你输入的信息是否正确!'
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', locals())
    
def post2db(request):
    if request.method=='POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            message='你的信息已经保存，要等管理员启用后才能看到'
            post_form.save()
            return HttpResponseRedirect('/list/')
        else:
            message='如果要张贴信息，那么每一个字段都要填......'
    else:
        post_form = forms.PostForm()
        message = '如果想要张贴信息，那么每一个字段都要填'
    return render(request, 'post2db.html', locals())

def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST['username'].strip()# 去点首尾空格
            login_password = request.POST['password']
            user = authenticate(username=login_name, password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, '成功登录了')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '账号尚未启用')
            else:
                messages.add_message(request, messages.WARNING, '登录失败')
        else:
            messages.add_message(request, messages.INFO, '请检查输入的字段内容')
    else:
        login_form = forms.LoginForm()
    return render(request, 'login.html', locals())
    
def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, '成功注销了')
    return redirect('/')

@login_required(login_url='/login/')    
def userinfo(request):
    if request.user.is_authenticated:
        username = request.user.username
    user = User.objects.get(username=username)
    try:
        profile = models.Profile.objects.get(user=user)
    except:
        profile = models.Profile(user=user)
    
    if request.method == 'POST':
        profile_form = forms.ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            messages.add_message(request, messages.INFO, "个人资料已存储")
            profile_form.save()
            return HttpResponseRedirect('/userinfo')
        else:
            messages.add_message(request, messages.INFO, '要修改资料，每一项都要填...')
    else:
        profile_form = forms.ProfileForm()
    
    return render(request, 'userinfo.html', locals())
    
    
      