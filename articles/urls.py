from django.conf.urls import url

from articles import views


urlpatterns = [
    url(r'^url/$', views.urltotag, name='urltotag'),
]
