from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from .tasks import send_annotation

class DiagnosisSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        obj = Diagnosis.objects.create(**validated_data)
        status, async_task = send_annotation(DiagId=obj.id, push=True)

        return Diagnosis(**validated_data)



    class Meta:
        model = Diagnosis
        fields = '__all__'
