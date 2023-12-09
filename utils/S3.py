import boto3
import logging
logger = logging.getLogger('mylogger')
from django.conf import settings
import os
class S3:
    def __init__(self, bucket_name):
        aws_access_key_id = settings.S3_SECRET_ID
        aws_secret_access_key = settings.S3_SECRET_KEY
        endpoint_url = settings.S3_ENDPOINT_URL
        # region = settings.S3_REGION # 区域

        # self.s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
        #                        aws_secret_access_key=aws_secret_access_key,
        #                        region_name=region,endpoint_url=endpoint_url)
        self.s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key,
                               endpoint_url=endpoint_url)

        self.bucket_name = bucket_name

    def upload_files(self, path_local, path_s3):
        """
        上传（重复上传会覆盖同名文件）
        :param path_local: 本地路径
        :param path_s3: s3路径（文件名， 就是s3仓库上的key）
        """
        if not self.upload_single_file(path_local, path_s3):
            return {'code': 200, 'message': '上传失败'}
        return {'code': 200, 'message': '上传成功'}

    def upload_single_file(self, src_local_path, dest_s3_path):
        """
        上传单个文件
        :param src_local_path:
        :param dest_s3_path:
        :return:
        """
        try:
            with open(src_local_path, 'rb') as f:
                self.s3_client.upload_fileobj(f, self.bucket_name, dest_s3_path)
        except Exception as e:
            logger.info(f'Upload data failed. | src: {src_local_path} | dest: {dest_s3_path} | Exception: {e}')
            return False
        logger.info(f'Uploading file successful. | src: {src_local_path} | dest: {dest_s3_path}')
        return True

    def get_filelist(self, path, filename):
        """
        Gets the object.

        :return: The object data in bytes.
        """
        try:
            save_path = os.path.join(settings.MEDIA_ROOT, path)

            objects = self.s3_client.list_objects_v2(Bucket=self.bucket_name)

            for obj in objects['Contents']:
                print(obj['Key'])

            logger.info(
                "Got object %s from bucket %s.",
                save_path,
                self.bucket_name,
            )
        except Exception as e:
            print(
                "Couldn't get object %s from bucket %s. Exception: %s" %
                ( path,
                self.bucket_name,
                e)
            )
            return False



