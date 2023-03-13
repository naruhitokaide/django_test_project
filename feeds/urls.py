from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_page,name="home_page" ),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('repositories/', views.repositories, name='repositories'),
]