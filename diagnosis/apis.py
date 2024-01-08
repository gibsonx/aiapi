# Create your views here.
from rest_framework import viewsets
from diagnosis.models import *
# from json import JSONEncoder
from diagnosis.serializers import DiagnosisSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

class DiagnoseViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosisSerializer
    queryset = Diagnosis.objects.all().order_by('-updated_at')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)





