from typing import List
import json
import urllib.request
from urllib.error import HTTPError
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aiapi.settings")
django.setup()
from django.conf import settings
import numpy as np
from PIL import Image
from utils.CvatEntity import *
from keras.models import load_model
import logging
logger = logging.getLogger('mylogger')
from utils.ImageProcesser import ImageProcesser
from utils.Oss2 import Oss2
def post(url, params, token=None):
    headers = {
        'Content-Type': 'application/json',
    }
    if token:
        headers['Authorization'] = 'Token {token}'.format(token=token)

    # Let's try to create our request with data, headers and method
    try:
        request = urllib.request.Request(url, data=params.encode('utf-8'), headers=headers, method='POST')
    except urllib.error.URLError as e:
        # Unable to create our request, here the reason
        return ("Unable to create youro request: {error}".format(error=str(e)))
    else:
        # We did create our request, let's try to use it
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            # An HTTP error occured, here the reason
            return ("HTTP Error: {error}".format(error=str(e)))
        except Exception as e:
            # We got another reason, here the reason
            return ("An error occured while trying to put {url}: {error}".format(
                url=url,
                error=str(e)
            ))
        else:
            # We are printing the result
            # We must decode it because response.read() returns a bytes string
            return (json.loads(response.read().decode('utf-8')))

def put(url, params, token=None):
    headers = {
        'Content-Type': 'application/json',
    }
    if token:
        headers['Authorization'] = 'Token {token}'.format(token=token)

    # Let's try to create our request with data, headers and method
    try:
        request = urllib.request.Request(url, data=params.encode('utf-8'), headers=headers, method='PUT')
    except urllib.error.URLError as e:
        # Unable to create our request, here the reason
        return ("Unable to create youro request: {error}".format(error=str(e)))
    else:
        # We did create our request, let's try to use it
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            # An HTTP error occured, here the reason
            return ("HTTP Error: {error}".format(error=str(e)))
        except Exception as e:
            # We got another reason, here the reason
            return ("An error occured while trying to put {url}: {error}".format(
                url=url,
                error=str(e)
            ))
        else:
            # We are printing the result
            # We must decode it because response.read() returns a bytes string
            return (json.loads(response.read().decode('utf-8')))


def get(url, token=None):
    headers = {
        'Content-Type': 'application/json',
    }
    if token:
        headers['Authorization'] = 'Token {token}'.format(token=token)

    try:
        print(headers)
        request = urllib.request.Request(url, headers=headers, method='GET')
    except urllib.error.URLError as e:
        # Unable to create our request, here the reason
        return ("Unable to create youro request: {error}".format(error=str(e)))
    else:
        # We did create our request, let's try to use it
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            # An HTTP error occured, here the reason
            return ("HTTP Error: {error}".format(error=str(e)))
        except Exception as e:
            # We got another reason, here the reason
            return ("An error occured while trying to put {url}: {error}".format(
                url=url,
                error=str(e)
            ))
        else:
            #  decode it because response.read() returns a bytes string
            return (json.loads(response.read().decode('utf-8')))


# def kps_inference(image_path):
#
#     model = load_model('C:\/Users\/Administrator\/Downloads\/pelvis.h5')
#
#     open_cv_image = np.stack([np.array(Image.open(image_path))])
#
#     kps = model.predict(open_cv_image)
#
#     row = kps.tolist()[0]
#
#     converted_keypoints = [list(a) for a in zip(*[iter(row)] * 2)]
#
#     return converted_keypoints


class CvatJobHelper:
    def __init__(self, jobid):
        self.username = settings.CVAT_USERNAME
        self.password = settings.CVAT_PASSWORD
        self.base_url = settings.CVAT_URL
        self.cvat_local_folder =  settings.CVAT_IMG_FOLDER_PREFIX
        self.jobid = jobid
        self.token = self.get_token()

    def get_token(self):
        auth = {
            "username": self.username,
            "password": self.password
        }
        auth_url = self.base_url + '/api/auth/login'
        token = post(auth_url, json.dumps(auth))['key']
        return token

    def removeprefix(self, text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        else:
            return text

    def get_jobImgOssPath(self):
        job_url = self.base_url + "/api/jobs/%d/data/meta?scheme=json" % self.jobid
        payload = get(job_url, self.token)
        img_path = self.removeprefix(payload['frames'][0]['name'],self.cvat_local_folder)
        return img_path

    def get_job_image(self):
        image_obj_path = self.get_jobImgOssPath()
        image_name = image_obj_path.split('/')[-1]

        target_folder, target_folder_relative = ImageProcesser.create_image_folder(dest_father_dir='images')

        target_image = os.path.join(target_folder, image_name)
        target_image_relative = os.path.join(target_folder_relative, image_name)

        oss = Oss2()
        oss.get_single_file(image_obj_path, target_image)

        return target_image, target_image_relative

    def create_kps_json_payload(self,kps: List) -> json:
        label_url = self.base_url + "/api/labels?job_id=%d" % self.jobid
        label_resp = get(label_url, self.token)
        sublabels = label_resp['results'][0]['sublabels']
        Ids = [ label['id'] for label in sublabels ]

        elements_list = []

        for z in zip(kps, Ids):
            b = Element()
            b.label_id = z[1]
            b.type = "points"
            b.frame = 0
            b.group = 0
            b.source = "manual"
            b.occluded = False
            b.outside = False
            b.z_order = 0
            b.rotation = float(0)
            b.points = z[0]
            b.attributes = []
            elements_list.append(b)

        s = Shapes(elements=elements_list)
        s.label_id = label_resp['results'][0]['id']
        s.type = "skeleton"
        s.frame = 0
        s.group = 0
        s.source = "manual"
        s.occluded = False
        s.outside = False
        s.z_order = 0
        s.rotation = float(0)
        s.points = []
        s.attributes = []
        a = Annotations(shapes=[s])
        json_data = json.dumps(a, default=lambda o: o.__dict__, indent=4)
        return json_data
    def post_anno(self, kps):
        json_data = self.create_kps_json_payload(kps)
        anno_url = self.base_url + "/api/jobs/%s/annotations" % self.jobid
        resp = put(anno_url, json_data, self.token)
        print(resp)


if __name__ == "__main__":
    job = CvatJobHelper(208)
    target_image, target_image_relative = job.get_job_image()

    annotated_image = ImageProcesser(image_path=target_image, model_args=settings.MODEL_DICT['SelfAssessAP10'])

    imgoi_array, kpsoi = annotated_image.kps_predict()
    kps = annotated_image.kpstuple_to_couplelist(kpsoi)
    print(job.post_anno(kps))

    # auth = {
    #     "username": "admin",
    #     "password": "9na6JucPkzP9"
    # }
    #
    # auth_url = 'http://8.217.95.207:8080/api/auth/login'
    # token = post(auth_url, json.dumps(auth))['key']
    #
    # label_url = 'http://8.217.95.207:8080/api/labels?job_id=47'
    # label_resp = get(label_url, token)
    #
    # sublabels = label_resp['results'][0]['sublabels']
    #
    # Ids = [ label['id'] for label in sublabels ]
    #
    # json_data = create_kps_json_payload(kps_inference('2023101401.jpg'),Ids)
    #
    # print(json_data)
    #
    # anno_url = 'http://8.217.95.207:8080/api/jobs/47/annotations'
    # resp = put(anno_url, json_data, token)
    # print(resp)
