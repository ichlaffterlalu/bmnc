from django.conf.urls import url
from .views import index, registrasi, login, logout

app_name = 'akun'
urlpatterns = [
    url(r'^$', index, name='landing-page'),
    url(r'registrasi', registrasi, name='registrasi'),
    url(r'login', login, name='login'),
    url(r'logout', logout, name='logout'),
]
