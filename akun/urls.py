from django.conf.urls import url
from django.views.generic.base import RedirectView
from .views import index, registrasi, login, logout

app_name = 'akun'
urlpatterns = [
    url(r'^$', RedirectView.as_view(url="/", permanent="False")),
    url(r'registrasi', registrasi, name='registrasi'),
    url(r'login', login, name='login'),
    url(r'logout', logout, name='logout'),
]
