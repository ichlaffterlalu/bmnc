from django.conf.urls import url
from .views import index, tambah_polling_berita, tambah_polling_biasa

app_name = 'polling'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^tambah_polling_berita', tambah_polling_berita, name='tambah_polling_berita'),
    url(r'^tambah_polling_biasa', tambah_polling_biasa, name='tambah_polling_biasa'),
]
