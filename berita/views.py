from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import connection
import datetime

from .models import Berita, Tag

def index(request):
    # todo : get narasumber data
    is_narasumber = True

    daftar_berita_raw = Tag.objects.raw("SELECT * FROM TAG;")
    daftar_berita = {}

    for item in daftar_berita_raw:
        if daftar_berita.get(item.tag) == None:
            daftar_berita[item.tag] = [item.url_berita]
        else:
            daftar_berita.get(item.tag).append(item.url_berita)

    html = 'berita/berita.html'
    response = {"is_narasumber":is_narasumber, "daftar_berita":daftar_berita}
    return render(request, html, response)

def tambah_berita(request):
    # todo : get narasumber data
    is_narasumber = True

    if is_narasumber:
        if request.method == 'GET':
            response = {}

            if 'tambah_berita' in request.session:
                response['tambah_berita'] = request.session.get('tambah_berita')
                del request.session['tambah_berita']

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
            id_universitas = 1 # todo : change from narasumber

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
                request.session['tambah_berita'] = 'Berhasil menambah berita'
            except:
                request.session['tambah_berita'] = 'Error ketika menambah berita (url sudah ada)'
            finally:
                c.close()

            return HttpResponseRedirect(reverse('berita:tambah_berita'))

    return HttpResponseRedirect('/')