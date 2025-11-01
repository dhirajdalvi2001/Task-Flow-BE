from django.urls import path, include

urlpatterns = [
    # custom APIs
    path('iam/', include('iam.urls')),
    path('tasks/', include('tasks.urls')),
]