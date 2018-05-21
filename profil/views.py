from django.shortcuts import render
from akun.models import Universitas, Narasumber, Dosen, Mahasiswa, Staf
from .models import Honor, Kupon

# Create your views here.
def index(request):
    request.session["id_narasumber"] = 1
    narasumber = Narasumber.objects.raw("SELECT * FROM NARASUMBER WHERE id = %s;", [request.session.get("id_narasumber")])[0]
    universitas = narasumber.id_universitas

    try: dosen = Dosen.objects.raw("SELECT * FROM DOSEN WHERE id_narasumber = %s;", [request.session.get("id_narasumber")])[0]
    except: dosen = None

    try: mahasiswa = Mahasiswa.objects.raw("SELECT * FROM MAHASISWA WHERE id_narasumber = %s;", [request.session.get("id_narasumber")])[0]
    except: mahasiswa = None

    try: staf = Staf.objects.raw("SELECT * FROM STAF WHERE id_narasumber = %s;", [request.session.get("id_narasumber")])[0]
    except: staf = None

    daftar_honor = Honor.objects.raw("SELECT * FROM HONOR WHERE id_narasumber = %s;", [request.session.get("id_narasumber")])
    daftar_kupon = Kupon.objects.raw("SELECT * FROM KUPON WHERE id_narasumber = %s;", [request.session.get("id_narasumber")])

    response = {"narasumber" : narasumber, "universitas" : universitas, "dosen" : dosen, "mahasiswa" : mahasiswa, "staf" : staf,
                "daftar_honor" : daftar_honor, "daftar_kupon" : daftar_kupon}
    html = "profil/lihat_profil.html"

    del request.session["id_narasumber"]

    return render(request, html, response)