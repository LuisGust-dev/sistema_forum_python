from django.urls import path
from perfil.views import editar_perfil, perfil_view

urlpatterns = [
    path('<slug:username>/', perfil_view, name='perfil'),
    path('editar-perfil/<slug:username>/', editar_perfil, name='editar-perfil'),
]