from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('challenge/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('submit_flag/<int:challenge_id>/', views.submit_flag, name='submit_flag'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('submission_error/', views.submission_error, name='submission_error'),
    path('submission_success/', views.submission_success, name='submission_success'),
    path('submission_fail/', views.submission_fail, name='submission_fail'),

]
