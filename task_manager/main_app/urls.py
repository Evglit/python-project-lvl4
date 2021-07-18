from django.urls import path
from task_manager.main_app import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('users/', views.UsersPage.as_view(), name='users'),
    path('users/create/', views.create_user, name='create'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('users/<int:user_id>/update/', views.update_user, name='update'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete'),
]