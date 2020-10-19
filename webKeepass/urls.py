"""webKeepass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.views import static  as view_static
from django.conf import settings
from portal.views import LogoutView, LoginView, bad_request, page_not_found

urlpatterns = [
    path('%s/' % settings.ADMIN_URL, admin.site.urls, name='admin'),  # 安全措施，防止admin外泄
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', include('dashboard.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/image/favicon.ico'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG == False:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', view_static.serve, {'document_root': settings.STATIC_ROOT }, name='static'),
    ]

handler400 = bad_request
handler404 = page_not_found
