from django.conf.urls import url

from . import views

urlpatterns = [
    url('^topics/(?P<unpass_id>\d+)/$', views.topics, name='topics'),
    url('^new_topic/(?P<unpass_id>\d+)/$', views.new_topic, name='new_topic'),
    url('^follow/(?P<topic_id>\d+)/$', views.follow, name='follow'),
    url('^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    url('^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
    url('^del_entry/(?P<entry_id>\d+)/$', views.del_entry, name='del_entry'),
]