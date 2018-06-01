from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import connection
from django.contrib import messages
import datetime

from akun.views import set_response
from .models import Berita, Tag

def index(request):
    is_narasumber = 'id_narasumber' in request.session

    daftar_berita_raw = Berita.objects.raw("SELECT * FROM BERITA ORDER BY created_at DESC;")
    daftar_tag_raw = [Tag.objects.raw("SELECT * FROM TAG WHERE url_berita=%s;", [x.url]) for x in daftar_berita_raw]

    daftar_berita = dict(zip(daftar_berita_raw, daftar_tag_raw))
    print(daftar_berita)
    html = 'berita/berita.html'

    response = {"is_narasumber": is_narasumber, "daftar_berita": daftar_berita}
    response = set_response(request, response)
    return render(request, html, response)

def tambah_berita(request):
    is_narasumber = 'id_narasumber' in request.session

    if is_narasumber:
        if request.method == 'GET':
            response = set_response(request, {})

            html = 'berita/membuat_berita.html'
            return render(request, html, response)

        elif request.method == 'POST':
            judul = request.POST.get('judul', '')[:100]
            url = request.POST.get('url', '')[:50]
            topik = request.POST.get('topik', '')[:100]
            try:
                jumlah_kata = int(request.POST.get('jumlah_kata'))
            except:
                jumlah_kata = 0
            tag = request.POST.get('tag', '')

            tag_list = [i.strip()[:50] for i in tag.split(';') if i.strip() != '']
            created_at = datetime.datetime.now()
            updated_at = datetime.datetime.now()
            rerata_rating = 0
            id_universitas = request.session['id_universitas']

            c = connection.cursor()
            try:
                c.execute('INSERT INTO Berita(url, judul, topik, created_at, \
                    updated_at, jumlah_kata, rerata_rating, id_universitas) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);',
                    [url, judul, topik, created_at, updated_at, \
                    jumlah_kata, rerata_rating, id_universitas])
                for i in tag_list:
                    c.execute('INSERT INTO Tag(url_berita, tag) \
                        VALUES (%s, %s);', [url, i])
                messages.success(request, 'Berhasil menambah berita')
            except:
                messages.error(request, 'Error ketika menambah berita (url sudah ada)')
            finally:
                c.close()

            return HttpResponseRedirect(reverse('berita:tambah_berita'))

    else:
        messages.error(request, 'Login terlebih dahulu untuk menambahkan berita')
        return HttpResponseRedirect(reverse('akun:login'))