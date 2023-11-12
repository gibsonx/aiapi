import boto3
import logging
logger = logging.getLogger('mylogger')
from django.conf import settings

class S3_upload():

    def __init__(self, bucket_name):
        aws_access_key_id = settings.TENCENT_SECRET_ID
        aws_secret_access_key = settings.TENCENT_SECRET_KEY
        endpoint_url = settings.TENCENT_S3_ENDPOINT_URL
        region = settings.TENCENT_S3_REGION # 区域

        self.s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key,
                               region_name=region,endpoint_url=endpoint_url)
        self.BUCKET_NAME = bucket_name

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
                self.s3.upload_fileobj(f, self.BUCKET_NAME, dest_s3_path)
        except Exception as e:
            logger.info(f'Upload data failed. | src: {src_local_path} | dest: {dest_s3_path} | Exception: {e}')
            return False
        logger.info(f'Uploading file successful. | src: {src_local_path} | dest: {dest_s3_path}')
        return True