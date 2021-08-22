from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path(
        'users/',
        views.UserListPage.as_view(),
        name='users'
    ),
    path(
        'users/create/',
        views.CreateUser.as_view(),
        name='create_user'
    ),
    path(
        'login/',
        views.LoginUser.as_view(),
        name='login'
    ),
    path(
        'logout/',
        views.LogoutUser.as_view(),
        name='logout'
    ),
    path(
        'users/<int:pk>/update/',
        views.UbdateUser.as_view(),
        name='update_user'
    ),
    path(
        'users/<int:pk>/delete/',
        views.DeleteUser.as_view(),
        name='delete_user'),  
]
