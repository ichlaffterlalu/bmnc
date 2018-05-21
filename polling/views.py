from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import connection
import datetime
from .models import PollingBiasa, PollingBerita

def index(request):
    is_narasumber = 'id_narasumber' in  request.session

    daftar_polling_biasa = PollingBiasa.objects.raw("SELECT * FROM POLLING_BIASA;")
    daftar_polling_berita = PollingBerita.objects.raw("SELECT * FROM POLLING_BERITA;")

    html = 'polling/polling.html'
    time_now = datetime.datetime.now()
    response = {"is_narasumber":is_narasumber, "daftar_polling_biasa":daftar_polling_biasa, "daftar_polling_berita":daftar_polling_berita, "time_now":time_now}
    return render(request, html, response)

def tambah_polling_berita(request):
    is_narasumber = 'id_narasumber' in request.session

    if is_narasumber:
        if request.method == 'GET':
            response = {}

            if 'tambah_polling_berita' in request.session:
                response['tambah_polling_berita'] = request.session.get('tambah_polling_berita')
                del request.session['tambah_polling_berita']

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

                    request.session['tambah_polling_berita'] = 'Berhasil menambah polling berita'
                except:
                    request.session['tambah_polling_berita'] = 'Error ketika menambah polling berita'
                finally:
                    c.close()
            else:
                request.session['tambah_polling_berita'] = 'Error ketika menambah polling berita (url berita tidak ada)'

            return HttpResponseRedirect(reverse('polling:tambah_polling_berita'))

    return HttpResponseRedirect('/')

def tambah_polling_biasa(request):
    is_narasumber = 'id_narasumber' in request.session

    if is_narasumber:
        if request.method == 'GET':
            response = {}

            if 'tambah_polling_biasa' in request.session:
                response['tambah_polling_biasa'] = request.session.get('tambah_polling_biasa')
                del request.session['tambah_polling_biasa']

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

                request.session['tambah_polling_biasa'] = 'Berhasil menambah polling biasa'
            except:
                request.session['tambah_polling_biasa'] = 'Error ketika menambah polling biasa'
            finally:
                c.close()

            return HttpResponseRedirect(reverse('polling:tambah_polling_biasa'))

    return HttpResponseRedirect('/')