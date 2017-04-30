"""SurviveLikeAStudentWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from SurviveLikeAStudentWeb import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login_page', views.loginPage, name='loginPage'),
    url(r'^login$', views.dedtest, name="login"),
    url(r'^registration/$', views.RegisterFormView.as_view()),
    url(r'^posts$', views.posts, name="posts"),
    url(r'^userlist$', views.usrlist, name="userlist"),
    url(r'^all_posts$', views.all_posts, name="all_posts"),
    url(r'^newpost$', views.newpost, name="newpost"),
    url(r'^game', views.game_page, name="game_page"),
    url(r'^get_score$', views.get_score, name="get_score"),
    url(r'^post/(?P<pk>[0-9]+)/$', views.curr_post, name='curr_post'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)-delete/$', views.delete, name='delete'),
    url(r'^profile_create$', views.profile_create, name="profile_create"),
    url(r'^profile_change$', views.profile_change, name="profile_change$"),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
