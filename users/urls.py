"""users URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path, path
from .views import UserHome, UserEdit, SignUpView, test_view, EditPreferences


app_name = 'users'
urlpatterns = [
    path('edit/', UserEdit.as_view(), name='edit'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('preferences/', EditPreferences.as_view(), name='preferences'),
    re_path(r'^(?P<username>[.+@_\w-]+)/$', UserHome.as_view(), name='home'),
    re_path(r'^test/(?P<ttt>[.+@_\w-]+)/$', test_view, name='test'),
    
]
