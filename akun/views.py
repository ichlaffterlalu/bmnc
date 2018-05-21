from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import connection
# Create your views here.
def index(request):
    pass


def login(request):
    if request.method == 'GET':
        response = {}
        html = 'akun/login.html'
        return render(request, html, response)

    elif request.method == 'POST' and 'id_narasumber' not in request.sessions:
        c = connection.cursor()
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        c.execute('SELECT * FROM PENGGUNA \
            WHERE username = %s AND password = %s;', [username,password])
        username = c.fetchone()[0]
        c.close()

        if username != None:
            request.session['id_narasumber'] = username.id_narasumber
            return HttpResponseRedirect(reverse('profil:index'))
        else:
            return HttpResponseRedirect(reverse('akun:login'))


def logout(request):
    del request.session
    return HttpResponseRedirect(reverse('akun:landing-page'))

def registrasi(request):

    if request.method == 'GET' :



    if request.method == 'POST':
            role = request.POST.get('role', '')
            username = request.POST.get('username', '')
            password = request.POST.get('topik', '')
            NoIdentitas = request.POST.get('NoIdentitas', '')
            nama = request.POST.get('nama', '')
            TempatLahir = request.POST.get('TempatLahir', '')
            TanggalLahir = request.POST.get('TanggalLahir', '')
            email = request.POST.get('email', '')
            nohp = request.POST.get('nohp', '')
            statusKemahasiswaan = request.POST.get('statusKemahasiswaan', '')
            idUniversitas = request.POST.get('idUniversitas', '')

            if role == :"Dosen" or role =="Staf":
                c = connection.cursor()
                try:
                    c.execute('SELECT id FROM narasumber ORDER BY id desc limit 1;')
                    lastId = c.fetchone()[0]
                    c.execute('INSERT INTO Narasumber(id, nama, email, tempat, tanggal, no_hp, jumlah_berita, rerata_kata, id_universitas) \
                        VALUES (%d, %s, %s, %s, %s, %s, %d, %d, %s);',
                        [lastID+1, nama, email, TempatLahir, TanggalLahir, nohp, 0, 0, idUniversitas])
                    
                    c.execute('INSERT INTO PENGGUNA(username, password, id) \
                        VALUES (%s, %s, %d);',
                        [username,password, lastID+1])
                    
                    request.session['registrasi'] = 'Berhasil menambah user'
                except:
                    request.session['registrasi'] = 'Error ketika menambah user (username sudah ada)'
                finally:
                    c.close()


            if role == "Mahasiswa":
                c = connection.cursor()
                try:
                    c.execute('SELECT id FROM narasumber ORDER BY id desc limit 1;')
                    lastId = c.fetchone()[0]
                    c.execute('INSERT INTO Narasumber(id, nama, email, tempat, tanggal, no_hp, jumlah_berita, rerata_kata) \
                        VALUES (%d, %s, %s, %s, %s, %s, %d, %d, %s);',
                        [lastID+1, nama, email, TempatLahir, TanggalLahir, nohp, 0, 0])

                    c.execute('INSERT INTO Mahasiswa(id_narasumber, npm,status) \
                        VALUES (%d, %d, %s);',
                        [lastID+1, NoIdentitas, statusKemahasiswaan])
                    
                    c.execute('INSERT INTO PENGGUNA(username, password, id) \
                        VALUES (%s, %s, %d);',
                        [username,password, lastID+1])
                    
                    request.session['registrasi'] = 'Berhasil menambah user'
                except:
                    request.session['registrasi'] = 'Error ketika menambah user (username sudah ada)'
                finally:
                    c.close()


            
            
            c = connection.cursor()
            try:
                c.execute('SELECT id FROM narasumber ORDER BY id desc limit 1;')
                lastId = c.fetchone()[0]
                c.execute('INSERT INTO Narasumber(id, nama, email, tempat, tanggal, no_hp, jumlah_berita, rerata_kata) \
                    VALUES (%d, %s, %s, %s, %s, %s, %d, %d);',
                    [lastID+1, nama, email, TempatLahir, TanggalLahir, nohp, 0, 0])
                
                c.execute('INSERT INTO PENGGUNA(username, password, id) \
                    VALUES (%s, %s, %d);',
                    [username,password, lastID+1])
                
                request.session['registrasi'] = 'Berhasil menambah user'
            except:
                request.session['registrasi'] = 'Error ketika menambah user (username sudah ada)'
            finally:
                c.close()

    return HttpResponseRedirect(reverse('profil:index'))