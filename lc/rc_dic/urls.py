from django.urls import path

from . import views

app_name = 'rc_dic'
urlpatterns = [
    path('', views.index, name='index'),
    path('lemmas', views.list_lemmas, name='list_lemmas'),
]
