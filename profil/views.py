from django.shortcuts import render
from django.contrib import messages
from akun.models import Universitas, Narasumber, Dosen, Mahasiswa, Staf
from .models import Honor, Kupon

from akun.views import set_response

# Create your views here.
def index(request):
    narasumber = Narasumber.objects.raw("SELECT * FROM NARASUMBER WHERE id = %s;", [request.session.get("id_narasumber")])[0]
    universitas = narasumber.id_universitas

    try: dosen = Dosen.objects.raw("SELECT * FROM DOSEN WHERE id_narasumber = %s;", [request.session.get("id_narasumber")])[0]
    except: dosen = None

    try: mahasiswa = Mahasiswa.objects.raw("SELECT * FROM MAHASISWA WHERE id_narasumber = %s;", [request.session.get("id_narasumber")])[0]
    except: mahasiswa = None

    try: staf = Staf.objects.raw("SELECT * FROM STAF WHERE id_narasumber = %s;", [request.session.get("id_narasumber")])[0]
    except: staf = None

    daftar_honor = Honor.objects.raw("SELECT * FROM HONOR WHERE id_narasumber = %s;", [request.session.get("id_narasumber")])
    try: daftar_honor[0]
    except: daftar_honor = None

    daftar_kupon = Kupon.objects.raw("SELECT * FROM KUPON WHERE id_narasumber = %s;", [request.session.get("id_narasumber")])
    try: daftar_kupon[0]
    except: daftar_kupon = None

    response = {"narasumber" : narasumber, "universitas" : universitas, "dosen" : dosen, "mahasiswa" : mahasiswa, "staf" : staf,
                "daftar_honor" : daftar_honor, "daftar_kupon" : daftar_kupon, "is_narasumber": 'id_narasumber' in request.session}
    response = set_response(request, response)
    html = "profil/lihat_profil.html"

    return render(request, html, response)