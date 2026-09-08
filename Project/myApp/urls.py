from django.urls import path
from .views import ContactCreatview
from . import views

urlpatterns = [
    path('home', views.home, name='index'),
    path('about', views.index, name='about'),
    path('accueil', views.accueil, name='accueil'),
    path('cv', views.cv, name='cv'),
    path('contact', ContactCreatview.as_view(), name='contact'),
]