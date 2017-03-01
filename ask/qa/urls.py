from django.conf.urls import url
from . import views

app_name = 'qa'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_controller, name='login'),
    url(r'^signup/$', views.signup_controller, name='testsignup'),
    url(r'^question/(?P<id>[0-9]+)/$', views.show_question, name='show_question'),
    url(r'^ask/$', views.add_ask, name='add_ask'),
    url(r'^popular/$', views.popular_questions, name='popular_questions'),
    url(r'^new/$', views.test, name='testnew'),
    url(r'^logout/$', views.logout_controller, name='logout'),
]
