from django.urls import path, include

from django.urls import path

from .views import *

urlpatterns = [
    path('', DiagnosisView,name="local_pic"),
    path('', DiagnosisView, name="cloud_pic"),
    path('job/', JoblistView.as_view(),name="joblist")
]