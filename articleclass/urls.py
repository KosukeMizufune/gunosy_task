from django.conf.urls import url
from articleclass import views

urlpatterns = [
    url(r'^url/$', views.url_list, name='url_list'),
]
