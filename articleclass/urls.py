from django.conf.urls import url

from articleclass import views


urlpatterns = [
    url(r'^url/$', views.urltotag, name='urltotag'),
]
