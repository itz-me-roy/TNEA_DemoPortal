from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from counseling import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('colleges/', views.college_list, name='college_list'),
    path('colleges/<int:pk>/', views.college_detail, name='college_detail'),
    path('cutoff-search/', views.cutoff_search, name='cutoff_search'),
    path('apply/<int:cutoff_id>/', views.apply_to_college, name='apply_to_college'),
]
