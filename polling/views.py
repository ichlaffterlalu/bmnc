from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import connection
from django.contrib import messages
import datetime

from akun.views import set_response
from .models import PollingBiasa, PollingBerita

def index(request):
    is_narasumber = 'id_narasumber' in request.session

    daftar_polling_biasa = PollingBiasa.objects.raw("SELECT * FROM POLLING_BIASA;")
    daftar_polling_berita = PollingBerita.objects.raw("SELECT * FROM POLLING_BERITA;")

    html = 'polling/polling.html'
    time_now = datetime.datetime.now()

    response = {"is_narasumber":is_narasumber, "daftar_polling_biasa":daftar_polling_biasa, "daftar_polling_berita":daftar_polling_berita, "time_now":time_now}
    response = set_response(request, response)
    return render(request, html, response)

def tambah_polling_berita(request):
    is_narasumber = 'id_narasumber' in request.session

    if is_narasumber:
        response = set_response(request, {})
        if request.method == 'GET':
            html = 'polling/membuat_polling_berita.html'
            return render(request, html, response)

        elif request.method == 'POST':
            c = connection.cursor()
            url_berita = request.POST.get('url_berita', '')[:50]
            c.execute('SELECT COUNT(*) FROM Berita \
                WHERE url = %s;', [url_berita])
            url_berita_exist = c.fetchone()[0] > 0
            c.close()

            if url_berita_exist:
                try:
                    polling_start = datetime.datetime(*[int(i) for i in request.POST.\
                        get('waktu_mulai').replace('T', '-').replace(':', '-').split('-')])
                except:
                    polling_start = datetime.datetime.now()
                try:
                    polling_end = datetime.datetime(*[int(i) for i in request.POST.\
                        get('waktu_selesai').replace('T', '-').replace(':', '-').split('-')])
                except:
                    polling_end = datetime.datetime.now()
                pertanyaan = request.POST.get('pertanyaan', '')

                pertanyaan_list = [i.strip()[:50] for i in pertanyaan.split(';') if i.strip() != '']
                total_responden = 0

                c = connection.cursor()
                try:
                    c.execute('SELECT COUNT(*) FROM Polling;')
                    id = c.fetchone()[0] + 1

                    c.execute('INSERT INTO Polling(id, polling_start, polling_end, \
                        total_responden) \
                        VALUES (%s, %s, %s, %s);',
                        [id, polling_start, polling_end, total_responden])
                    c.execute('INSERT INTO Polling_Berita(id_polling, url_berita) \
                        VALUES (%s, %s);', [id, url_berita])
                    for i in pertanyaan_list:
                        jumlah_dipilih = 0
                        c.execute('INSERT INTO Respon(id_polling, jawaban, jumlah_dipilih) \
                            VALUES (%s, %s, %s);', [id, i, jumlah_dipilih])

                    messages.success(request, 'Berhasil menambah polling berita')
                except:
                    messages.error(request, 'Error ketika menambah polling berita')
                finally:
                    c.close()
            else:
                messages.error(request, 'Error ketika menambah polling berita (url berita tidak ada)')

            return HttpResponseRedirect(reverse('polling:tambah_polling_berita'))

    else:
        messages.error(request, 'Login terlebih dahulu untuk menambahkan polling berita')
        return HttpResponseRedirect(reverse('akun:login'))

def tambah_polling_biasa(request):
    is_narasumber = 'id_narasumber' in request.session

    if is_narasumber:
        response = set_response(request, {})
        if request.method == 'GET':
            response = set_response(request, {})

            html = 'polling/membuat_polling_biasa.html'
            return render(request, html, response)

        elif request.method == 'POST':
            deskripsi = request.POST.get('deskripsi', '')[:100]
            try:
                polling_start = datetime.datetime(*[int(i) for i in request.POST.\
                    get('waktu_mulai').replace('T', '-').replace(':', '-').split('-')])
            except:
                polling_start = datetime.datetime.now()
            try:
                polling_end = datetime.datetime(*[int(i) for i in request.POST.\
                    get('waktu_selesai').replace('T', '-').replace(':', '-').split('-')])
            except:
                polling_end = datetime.datetime.now()
            pertanyaan = request.POST.get('pertanyaan', '')

            pertanyaan_list = [i.strip()[:50] for i in pertanyaan.split(';') if i.strip() != '']
            total_responden = 0

            c = connection.cursor()
            try:
                c.execute('SELECT COUNT(*) FROM Polling;')
                id = c.fetchone()[0] + 1

                c.execute('INSERT INTO Polling(id, polling_start, polling_end, \
                    total_responden) \
                    VALUES (%s, %s, %s, %s);',
                    [id, polling_start, polling_end, total_responden])
                url = 'http://url-random/' + str(id)
                c.execute('INSERT INTO Polling_Biasa(id_polling, url, deskripsi) \
                    VALUES (%s, %s, %s);', [id, url, deskripsi])
                for i in pertanyaan_list:
                    jumlah_dipilih = 0
                    c.execute('INSERT INTO Respon(id_polling, jawaban, jumlah_dipilih) \
                        VALUES (%s, %s, %s);', [id, i, jumlah_dipilih])

                messages.success(request, 'Berhasil menambah polling biasa')
            except:
                messages.error(request, 'Error ketika menambah polling biasa')
            finally:
                c.close()
            return HttpResponseRedirect(reverse('polling:tambah_polling_biasa'))

    else:
        messages.error(request, 'Login terlebih dahulu untuk menambahkan polling biasa')
        return HttpResponseRedirect(reverse('akun:login'))