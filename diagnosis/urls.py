from django.urls import path, include

from django.urls import path

from .views import *
from .apis import *

urlpatterns = [
    path('', DiagnosisView,name="local_pic"),
    path('jobsubmit/', JobDiagnosisView, name="cloud_pic"),
    path('job/', JoblistView.as_view(),name="joblist"),
    path('api/', DiagnoseViewSet.as_view({'get': 'list', 'post': 'create'}), name='diag_list'),
    path('api/job/<uuid:pk>/', DiagnoseViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}),
         name='diag_detail')
]