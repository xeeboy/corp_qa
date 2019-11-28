from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^up(?P<batch>.+)/$', views.unpass, name='unpass'),
    url(r'^p(?P<keyword>.+)/$', views.performance, name='performance'),
    url(r'^$', views.index, name='index'),
    url(r'^search$', views.home_search, name='home_search'),
    url(r'^all_unpass$', views.all_unpass, name='all_unpass'),
    url(r'^all_suggestion$', views.all_suggestion, name='all_suggestion'),
    url(r'^dw_api$', views.chat_reply, name='chat_reply'),
]