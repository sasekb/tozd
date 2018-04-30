"""users URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.views import LoginView
from .views import UserHome, UserEdit, SignUpView, test_view, EditPreferences, logout_view



urlpatterns = [
    url(r'^edit/$', UserEdit.as_view(), name='edit'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^login/$', LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^preferences/$', EditPreferences.as_view(), name='preferences'),
    url(r'^(?P<username>[.+@_\w-]+)/$', UserHome.as_view(), name='home'),
    url(r'^test/(?P<ttt>[.+@_\w-]+)/$', test_view, name='test'),
]
