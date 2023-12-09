# -*- coding: utf-8 -*-
import oss2
import logging
logger = logging.getLogger('mylogger')
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aiapi.settings")
django.setup()
from django.conf import settings
import shutil
class Oss2:
    def __init__(self):
        accessKeyId = settings.S3_SECRET_ID
        accessKeySecret = settings.S3_SECRET_KEY
        accessEndpoint = settings.S3_ENDPOINT_URL
        # 使用代码嵌入的RAM用户的访问密钥配置访问凭证。
        auth = oss2.Auth(accessKeyId, accessKeySecret)
        self.bucket = oss2.Bucket(auth, accessEndpoint, settings.S3_BUCKET)

    def get_single_file(self,oss_obj, target_file):
        try:
            self.bucket.get_object_to_file(oss_obj,target_file)
        except oss2.exceptions.NoSuchKey as e:
            print('status={0}, request_id={1}'.format(e.status, e.request_id))

    # def get_job_image(self,jobid):
    #     airequest = CvatHelper(settings.CVAT_USERNAME,
    #                            settings.CVAT_PASSWORD,
    #                            settings.CVAT_URL)
    #     image_obj_path = airequest.get_jobImgOssPath(jobid, settings.CVAT_IMG_FOLDER_PREFIX)
    #     image_name = image_obj_path.split('/')[-1]
    #
    #     target_folder, target_folder_relative = ImageProcesser.create_image_folder(dest_father_dir='images')
    #
    #     target_image = os.path.join(target_folder, image_name)
    #     target_image_relative = os.path.join(target_folder_relative, image_name)
    #
    #     self.get_single_file(image_obj_path, target_image)
    #
    #     return target_image, target_image_relative

if __name__ == '__main__':
    oss2 = Oss2()
    # oss2.get_single_file(
    #     oss_obj='analysis/dynamicCarriageOvercrossingLowerBrace/2023/06/24/1672458184679751680_上交叉-下蹲.jpg',
    #     target_file=r'C:\Users\Administrator\PycharmProjects\aiapi\media\images\1672458184679751680_上交叉-下蹲.jpg'
    # )
    # oss2.get_job_image(jobid=103)