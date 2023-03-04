from django.urls import path
from statuses.views import CreateStatusView, index, UpdateStatusView, DeleteStatusView

urlpatterns = [
    path('', index, name='statuses'),
    path('create/', CreateStatusView.as_view(), name='create_status'),
    path('<int:pk>/update/', UpdateStatusView.as_view(), name='update_status'),
    path('<int:pk>/delete/', DeleteStatusView.as_view(), name='delete_status'),
]