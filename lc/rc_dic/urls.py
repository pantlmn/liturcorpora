from django.urls import path

from . import views

app_name = 'rc_dic'
urlpatterns = [
    path('', views.index, name='index'),
    path('ruscorpora', views.index, name='index'),
    path('ruscorpora/lemmas', views.list_lemmas, name='list_lemmas'),
]
