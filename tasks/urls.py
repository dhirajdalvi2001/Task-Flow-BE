from django.urls import path

urlpatterns = [
    path('', TaskListDetailView.as_view(), name='task-list'),
    path('<uuid:id>/', TaskListDetailView.as_view(), name='task-detail'),
    path('create/', TaskListDetailView.as_view(), name='task-create'),
    path('update/<int:id>/', TaskListDetailView.as_view(), name='task-update'),
    path('delete/<int:id>/', TaskListDetailView.as_view(), name='task-delete'),
]