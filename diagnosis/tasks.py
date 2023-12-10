from celery import Celery
from celery.schedules import crontab
import time
import os
from celery import Celery
from django.conf import settings
from celery import shared_task
# 设置django环境变量
from aiapi.celery_factory import app
# 普通任务 由 方法名 send_email.delay()触发
from typing import List,Dict,Tuple
from diagnosis.models import Diagnosis
from utils.CvatHelper import CvatJobHelper
from utils.ImageProcesser import ImageProcesser
@shared_task()
def send_annotation(jobId: int, type: str) -> Tuple[bool, str]:
    """
    This function is used to send annotations to CVAT and save the annotated image.
    If the process is successful, it returns True and the string "success".
    Otherwise, if an exception occurs, it prints the exception and returns False and the exception.
    1. query image path on CVAT per job and download the image to local for prediction with CvatJobHelper
    2. choose model according to diagnosis type Id and inference keypoionts in form of list[Keypoint]
    3. save annotated image local and path in DB for web display.
    4. use CvatJobHelper again to post predicted keypoints onto the CVAT
    """

    # Create a CvatJobHelper instance with the jobid from the Diagnosis object
    job = CvatJobHelper(jobId)
    # Retrieve the target image and its relative path
    target_image, target_image_relative = job.get_job_image()

    # Depending on the diagnosis type of the Diagnosis object, create an ImageProcesser instance with the appropriate model arguments
    if type == "1":
        annotated_image = ImageProcesser(image_path=target_image, model_args=settings.MODEL_DICT['SelfAssessAP10'])
    elif type == "2":
        annotated_image = ImageProcesser(image_path=target_image, model_args=settings.MODEL_DICT['SelfAssessLT5'])
    elif type== "3":
        annotated_image = ImageProcesser(image_path=target_image, model_args=settings.MODEL_DICT['Pivles'])

    # Predict keypoints on the image and convert them into a list of tuples
    imgoi_array, kpsoi = annotated_image.kps_predict()
    kps = annotated_image.kpstuple_to_couplelist(kpsoi)

    print("mark annotations on cvat with payload", job.post_anno(kps))
    anno_path = annotated_image.save_tran_image()
    # If the saving is successful, update the Diagnosis object with the relative path of the target image and the path of the annotated image
    if anno_path:
        obj = Diagnosis.objects.get(jobid=jobId)
        obj.img=target_image_relative
        obj.anno_img = annotated_image.save_tran_image()
        try:
            obj.save()
            return True, "success"
        except Exception as e:
            print(e)
            return False, e
