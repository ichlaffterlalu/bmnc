"""bmnc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import akun.urls as akun
import berita.urls as berita
import profil.urls as profil
import polling.urls as polling

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^akun/', include(akun)),
	url(r'^berita/', include(berita)),
	url(r'^profil/', include(profil)),
	url(r'^polling/', include(polling)),
	url(r'^$', RedirectView.as_view(url="/berita/", permanent="False"), name='index')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
