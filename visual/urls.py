from django.conf.urls import url

from visual import views

urlpatterns = [
    url('^fpy$', views.fpy_60_days, name='fpy'),
    url('^upkeys$', views.up_keys, name='up_keys')
]