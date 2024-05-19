from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from apps.vcenter.views.v1 import CreateVMView

urlpatterns = [
    path('create-machine/', CreateVMView.as_view(), name='create_machine'),
    path('edit-machine/<str:vm_name>/', CreateVMView.as_view(), name='update_machine'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
