from django.urls import path

from . import views

app_name = 'rc_dic'
urlpatterns = [
    path('', views.index, name='index'),
    path('robots.txt', views.robots, name='robots'),
    path('ruscorpora/', views.index, name='index'),
    path('ruscorpora/find/', views.find_word, name='find_word'),
    path('ruscorpora/lemmas/', views.list_lemmas, name='list_lemmas'),
    path('ruscorpora/lemmas/<int:lemma_id>/', views.lemma_info, name='lemma_info'),
]
