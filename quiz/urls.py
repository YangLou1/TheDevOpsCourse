from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<quiz>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<quiz>\d+)/submit$', views.submit, name='submit'),
    url(r'^(?P<quiz>\d+)/result$', views.result, name='result'),
    url(r'^lesson/$', views.lesson, name='lesson')
]
