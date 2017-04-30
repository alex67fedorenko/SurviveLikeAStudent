# -*- coding: utf-8 -*-
import json

from SurviveLikeAStudentWeb.forms import LoginForm, PostForm, ProfileForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.utils import timezone
from SurviveLikeAStudentWeb.models import Post, Profile
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.views.generic import ListView


def home(request):
    auth.logout(request)
    return render_to_response('home.html')


def loginPage(request):
    auth.logout(request)
    form = LoginForm()
    return render_to_response('login.html', {'form': form})


def dedtest(request):
    if request.GET.get('login'):
        login = request.GET['login']
    else:
        return render_to_response('error.html', {
            'back': '/',
            'error': 'Enter the login!'
        })
    if request.GET.get('passw'):
        passw = request.GET['passw']
    else:
        return render_to_response('error.html', {
            'back': '/',
            'error': 'Enter the password!'
        })
    uuser = auth.authenticate(username=login, password=passw)
    if uuser:
        auth.login(request, uuser)
        id = User.objects.get(username__iexact=uuser).id
        table = Post.objects.filter(author=id).order_by('published_date')  # Получаем список постов по имени
        # a = dict(posts=table, current=True)  # передаем посты в шаблон
        try:
            profile = Profile.objects.filter(user=id)
            a = dict(posts=table, current=True, profile=profile[0], notcreate=False)
            return render(request, 'postlist.html', a)
        except:
            a = dict(posts=table, current=True, notcreate=True)
            return render_to_response('postlist.html', a)
    else:
        return render_to_response('error.html', {
            'back': '/',
            'error': 'Error! Incorrect login or password...'
        })


def usrlist(request):
    if 'logout' in request.GET:
        auth.logout(request)
    table = User.objects.all()
    if request.user.is_authenticated():
        a = dict(users=table, where='Logout')
    else:
        a = dict(users=table, where='Exit')
    return render_to_response('userlist.html', a)


def posts(request):
    current = auth.get_user(request)
    if request.GET.get('username'):
        name = request.GET['username']
        user = User.objects.get(username__iexact=name)
        id = user.id
        table = Post.objects.filter(author=id).order_by('-published_date')
        test = current == user
    else:
        table = Post.objects.filter(author=current.id).order_by('-published_date')
        test = True
    try:
        name = request.GET['username']
        user = User.objects.get(username__iexact=name)
        profile = Profile.objects.filter(user=user)
        a = dict(posts=table, current=test, profile=profile[0], notcreate=False)
        return render(request, 'postlist.html', a)
    except:
        a = dict(posts=table, current=test, notcreate=True)
        return render(request, 'postlist.html', a)


def newpost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('curr_post', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'newpost.html', {'form': form, 'who': request.user})


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "registration.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


def curr_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'curr_post.html', {'post': post})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('curr_post', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'newpost.html', {'form': form, 'who': request.user})


def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    #return redirect('posts')
    return render_to_response('error.html', {
            'back': '/',
            'error': 'Your feedback was deleted.',
            'deletion': True,
            'who': request.user
        })


def profile_create(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                '''
                profile.image = form.cleaned_data['image']
                profile.full_name = form.cleaned_data['full_name']
                profile.phone = form.cleaned_data['phone']
                profile.about = form.cleaned_data['about']
                profile.email = form.cleaned_data['email']
                '''
                profile.save()
                # return redirect('posts?username='+str(request.user))
                # HttpResponseRedirect(reverse('posts?username=', args=(request.user,)))
                return redirect('/posts?username=' + str(request.user))
        else:
            form = ProfileForm()
        return render(request, 'profileedit.html', {'form': form, 'who': request.user, 'notcreate': True})
    else:
        raise Http404


def profile_change(request):
    profile = get_object_or_404(Profile, user=request.user.id)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('/posts?username=' + str(request.user))
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profileedit.html', {'form': form, 'who': request.user, 'notcreate': False})


def all_posts(request):
    table = Post.objects.order_by('-published_date')
    paginator = Paginator(table, 3)
    page = request.GET.get('page')
    try:
        post_list_page = paginator.page(page)
    except PageNotAnInteger:
        post_list_page = paginator.page(1)
    except EmptyPage:
        post_list_page = paginator.page(paginator.num_pages)
    return render(request, 'all_posts.html', {'posts': post_list_page})


def game_page(request):
    # Profile.objects.get(user=request.user).update(score=6)
    # obj = Profile.objects.get(user=request.user.id)
    # obj.score = 0
    # obj.save()

    return render(request, 'WebBuild-18-03-17.html', {'who': request.user})


def get_score(request):
    # obj = Profile.objects.get(user=request.user.id)
    # obj.score = 11
    # obj.save()
    # profile = get_object_or_404(Profile, user=request.user.id)
    # profile.score = 6
    # profile.save()
    # if request.method == "POST":
    #     body_unicode = request.body.decode('utf-8')
    #     body = json.loads(body_unicode)
    #     content = body['score']
    #     profile.score = content
    #     profile.save()

    if request.GET.get('score'):
        obj = Profile.objects.get(user=request.user.id)
        obj.score = int(request.GET['score'])
        obj.save()
    return HttpResponse('success')

    # if request.method == 'POST':
    #     if 'score' in request.POST:
    #         score = request.POST['score']
    #         # doSomething with pieFact here...
    #         return HttpResponse('success')  # if everything is OK
    #         # nothing went well
    # return HttpResponse('FAIL!!!!!')
