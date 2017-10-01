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
from .views import OrdersList, ProcessOrder, DeliveriesDistributerList, DeliveriesAllList, DeliverOrder



urlpatterns = [
    url(r'^orders/$', OrdersList.as_view(), name='orders'),
    url(r'^order/(?P<order>[\d]+)$', ProcessOrder.as_view(), name='process'),
    url(r'^distribution/$', DeliveriesDistributerList.as_view(), name='deliveries'),
    url(r'^distribution/all$', DeliveriesAllList.as_view(), name='deliveries_all'),
    url(r'^distribution/(?P<package>[\d]+)$', DeliverOrder.as_view(), name='deliver'),
    # url(r'^signup/$', signup, name='signup'),
    # url(r'^login/$', LoginView.as_view(template_name='users/login.html'), name='login'),
    # url(r'^(?P<username>[.+@_\w-]+)/$', UserHome.as_view(), name='home'),
    # url(r'^test/(?P<ttt>[.+@_\w-]+)/$', test_view, name='test'),
]
