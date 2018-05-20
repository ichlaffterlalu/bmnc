from django.conf.urls import url
from .views import index, tambah_berita

app_name = 'berita'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^tambah_berita', tambah_berita, name='tambah_berita'),
]
