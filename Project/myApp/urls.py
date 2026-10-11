from django.urls import path
from .views import ContactCreatview
from . import views

urlpatterns = [
    path('', views.cv, name='root'),
    path('dashboard/login/', views.DashboardLoginView.as_view(), name='dashboard_login'),
    path('dashboard/logout/', views.DashboardLogoutView.as_view(), name='dashboard_logout'),
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/profile/', views.dashboard_profile_edit, name='dashboard_profile_edit'),
    path('dashboard/sections/<slug:key>/', views.dashboard_section, name='dashboard_section'),
    path('dashboard/sections/<slug:key>/edit/', views.dashboard_section_edit, name='dashboard_section_edit'),
    path('dashboard/sections/<slug:key>/items/add/', views.dashboard_item_create, name='dashboard_item_create'),
    path('dashboard/items/<int:item_id>/edit/', views.dashboard_item_edit, name='dashboard_item_edit'),
    path('dashboard/items/<int:item_id>/delete/', views.dashboard_item_delete, name='dashboard_item_delete'),
    path('about', views.index, name='about'),
    path('cv', views.cv, name='cv'),
    path('contact', ContactCreatview.as_view(), name='contact'),
]