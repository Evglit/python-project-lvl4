from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.UserListPage.as_view(),
        name='users'
    ),
    path(
        'create/',
        views.CreateUser.as_view(),
        name='create_user'
    ),
    path(
        '<int:pk>/update/',
        views.UbdateUser.as_view(),
        name='update_user'
    ),
    path(
        '<int:pk>/delete/',
        views.DeleteUser.as_view(),
        name='delete_user'),
]
