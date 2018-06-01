from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import connection
from django.contrib import messages
from hashlib import sha512

# Create your views here.
def index(request):
    response = {}
    if 'username' not in request.session:
        html = 'akun/landing_page.html'
        return render(request, html, response)
    else:
        response = set_response(request, response)
        return HttpResponseRedirect(reverse('berita:index'))

def login(request):
    if request.method == 'GET' and 'username' not in request.session:
        response = {}
        html = 'akun/login.html'
        return render(request, html, response)

    elif request.method == 'POST' and 'username' not in request.session:
        c = connection.cursor()
        username = request.POST.get('username', '')
        password = sha512(request.POST.get('password', '').encode()).hexdigest()
        c.execute('SELECT * FROM PENGGUNA \
            WHERE username = %s AND password = %s;', [username, password])
        user_data = c.fetchone()
        c.close()

        if username != None:
            request.session['username'] = user_data[0]
            request.session['id_narasumber'] = user_data[2]

            c = connection.cursor()
            c.execute('SELECT nama, id_universitas FROM NARASUMBER \
            WHERE id = %s;', [user_data[2]])
            narasumber_data = c.fetchone()
            request.session['nama_narasumber'] = narasumber_data[0]
            request.session['id_universitas'] = narasumber_data[1]

            messages.success(request, 'Berhasil login.')
            return HttpResponseRedirect(reverse('berita:index'))

        else:
            messages.error(request, 'Login gagal. Cek kembali username dan password yang diberikan.')
            return HttpResponseRedirect(reverse('akun:login'))
    else:
        messages.warning(request, 'Anda sudah login.')
        return HttpResponseRedirect(reverse('berita:index'))

def set_response(request, response):
    response['username'] = request.session.get('username')
    response['id_narasumber'] = request.session.get('id_narasumber')
    response['nama_narasumber'] = request.session.get('nama_narasumber')
    response['id_universitas'] = request.session.get('id_universitas')
    return response

def logout(request):
    if request.session.get('username') != None: del request.session['username']
    if request.session.get('id_narasumber') != None: del request.session['id_narasumber']
    if request.session.get('nama_narasumber') != None: del request.session['nama_narasumber']
    if request.session.get('id_universitas') != None: del request.session['id_universitas']
    return HttpResponseRedirect("/")

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
            return HttpResponseRedirect("/")
        finally:
            c.close()