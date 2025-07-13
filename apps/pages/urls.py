from django.urls import path 
from pages import views

urlpatterns = [
    path('', views.paginas_view, name='home'), 
    path('sobre/', views.paginas_view, name='sobre'), 
   
]
