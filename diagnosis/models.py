import uuid
from django.db import models


class Diagnosis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jobid = models.IntegerField(null=True,blank=True,verbose_name="打点任务ID")
    img = models.ImageField(upload_to='images/%Y/%m/%d',verbose_name='图片',null=True,blank=True)
    anno_img = models.ImageField(upload_to='anno_images/', verbose_name='打点图片',null=True,blank=True)
    type = models.IntegerField(verbose_name="打点类型",default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}'s created"




