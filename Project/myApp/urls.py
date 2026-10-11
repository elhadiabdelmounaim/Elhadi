from django.urls import path
from .views import ContactCreatview
from . import views

urlpatterns = [
    path('', views.cv, name='root'),
    path('about', views.index, name='about'),
    path('cv', views.cv, name='cv'),
    path('contact', ContactCreatview.as_view(), name='contact'),
]