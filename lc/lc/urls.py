from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('rc_dic.urls')),
    path('ruscorpora/', include('rc_dic.urls')),
    path('admin/', admin.site.urls),
]
