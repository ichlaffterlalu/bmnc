from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import connection
from django.contrib import messages
from hashlib import sha512

# Create your views here.
def index(request):
    response = {}
    html = 'akun/landing page.html'
    return render(request, html, response)

def login(request):
    if request.method == 'GET':
        response = {}
        html = 'akun/login.html'
        return render(request, html, response)

    elif request.method == 'POST' and 'id_narasumber' not in request.session:
        c = connection.cursor()
        username = request.POST.get('username', '')
        password = sha512(request.POST.get('password', '').encode()).hexdigest()
        c.execute('SELECT * FROM PENGGUNA \
            WHERE username = %s AND password = %s;', [username, password])
        username = c.fetchone()
        c.close()

        if username != None:
            request.session['id_narasumber'] = username[2]
            c = connection.cursor()
            c.execute('SELECT id_universitas FROM NARASUMBER \
            WHERE id = %s;', [username[2]])
            request.session['id_universitas'] = c.fetchone()[0]
            messages.success(request, 'Berhasil login.')
            return HttpResponseRedirect(reverse('profil:index'))
        else:
            messages.error(request, 'Login gagal. Cek kembali username dan password yang diberikan.')
            return HttpResponseRedirect(reverse('akun:login'))
    elif request.method == 'POST':
        messages.warning(request, 'Anda sudah login.')
        return HttpResponseRedirect(reverse('profil:index'))


def logout(request):
    del request.session['id_narasumber']
    del request.session['id_universitas']
    return HttpResponseRedirect(reverse('akun:landing-page'))

def registrasi(request):
    if request.method == 'GET':
        response = {}
        html = "akun/registrasi.html"
        return render(request, html, response)

    if request.method == 'POST':
        role = request.POST.get('role', '')
        username = request.POST.get('username', '')
        password = sha512(request.POST.get('password', '').encode()).hexdigest()
        noIdentitas = request.POST.get('noIdentitas', '')
        nama = request.POST.get('nama', '')
        tempatLahir = request.POST.get('tempatLahir', '')
        tanggalLahir = request.POST.get('tanggalLahir', '')
        email = request.POST.get('email', '')
        noHp = request.POST.get('noHp', '')
        idUniversitas = request.POST.get('idUniversitas', '')

        c = connection.cursor()

        try:
            c.execute('SELECT id FROM narasumber ORDER BY id desc limit 1;')
            lastId = c.fetchone()[0]

            c.execute('INSERT INTO Narasumber(id, nama, email, tempat, tanggal, no_hp, jumlah_berita, rerata_kata, id_universitas) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);',
                        [lastId+1, nama, email, tempatLahir, tanggalLahir, noHp, 0, 0, idUniversitas])

            if role == "Mahasiswa":
                statusKemahasiswaan = request.POST.get('statusKemahasiswaan', '')
                c.execute('INSERT INTO Mahasiswa(id_narasumber, npm, status) \
                    VALUES (%s, %s, %s);',
                    [lastId+1, noIdentitas, statusKemahasiswaan])

            elif role == "Dosen":
                jurusan = request.POST.get('jurusan', '')
                c.execute('INSERT INTO Dosen(id_narasumber, nik_dosen, jurusan) \
                    VALUES (%s, %s, %s);',
                    [lastId+1, noIdentitas, jurusan])

            elif role == "Staf":
                posisi = request.POST.get('posisi', '')
                c.execute('INSERT INTO Staf(id_narasumber, nik_staf, posisi) \
                    VALUES (%s, %s, %s);',
                    [lastId+1, noIdentitas, posisi])

            c.execute('INSERT INTO PENGGUNA(username, password, id_narasumber) \
                        VALUES (%s, %s, %s);',
                        [username, password, lastId+1])

            messages.success(request, 'Berhasil menambah user')
            return HttpResponseRedirect("/")
        except:
            messages.error(request, 'Error ketika menambah user (username sudah ada)')
            return HttpResponseRedirect("/akun/registrasi")
        finally:
            c.close()