from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from apps.vcenter import views

urlpatterns = [
    path('create-machine/', views.CreateVMView.as_view()),
    path('edit-machine/<str:vm_name>/', views.CreateVMView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
