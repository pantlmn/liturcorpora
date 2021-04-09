from django.urls import path

from . import views

app_name = 'hymns'
urlpatterns = [
    path('', views.index, name='index'),
    path('blocks/<int:block_id>/', views.index, name='blocks'),
    path('par/<int:paragraph_id>/', views.paragraph, name='par'),
]
