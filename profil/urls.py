from django.conf.urls import url
from .views import index
#url for app
app_name = 'profil'
urlpatterns = [
    url(r'^$', index, name='index'),
]
