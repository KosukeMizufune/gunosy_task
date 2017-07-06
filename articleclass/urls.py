from django.conf.urls import url
from articleclass import views


# URL
urlpatterns = [
    url(r'^url/$', views.url_list, name='url_list'),
]
