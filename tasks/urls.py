from django.urls import path
from .views import TaskListCreateView, TaskSequenceView, TaskDetailsUpdateDeleteView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('change-sequence/', TaskSequenceView.as_view(), name='task-change-sequence'),
    # path('<uuid:id>/', TaskListDetailView.as_view(), name='task-detail'),
    path('<uuid:id>/', TaskDetailsUpdateDeleteView.as_view(), name='task-details-update-delete'),
]