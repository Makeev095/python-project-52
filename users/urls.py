from django.urls import path
from users.views import RegisterUser, UpdateUser, DeleteUser, UserList

urlpatterns = [
    path('', UserList.as_view(), name='users'),
    path('create/', RegisterUser.as_view(), name='create_user'),
    path('<int:pk>/update/', UpdateUser.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteUser.as_view(), name='delete'),
]