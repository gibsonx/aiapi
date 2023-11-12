from typing import List
import json
import urllib.request
from typing import List
from urllib.error import HTTPError

import numpy as np
from PIL import Image
from CvatEntity import *
from keras.models import load_model

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


def create_kps_json_payload(kps: List, labels: List) -> json:

    elements_list = []

    for z in zip(kps,labels):
        sublabel = Elements()
        sublabel.label_id = z[1]
        sublabel.type = "points"
        sublabel.frame = 0
        sublabel.group = 0
        sublabel.source = "manual"
        sublabel.occluded = False
        sublabel.outside = False
        sublabel.z_order = 0
        sublabel.rotation = float(0)
        sublabel.points = z[0]
        sublabel.attributes = []
        elements_list.append(sublabel)

    s = Shapes()
    s.elements = elements_list
    s.label_id = 1
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


def kps_inference(image_path):

    model = load_model('C:\/Users\/Administrator\/Downloads\/pelvis.h5')

    open_cv_image = np.stack([np.array(Image.open(image_path))])

    kps = model.predict(open_cv_image)

    row = kps.tolist()[0]

    converted_keypoints = [list(a) for a in zip(*[iter(row)] * 2)]

    return converted_keypoints

if __name__ == "__main__":
    auth = {
        "username": "admin",
        "password": "9na6JucPkzP9"
    }

    auth_url = 'http://8.217.95.207:8080/api/auth/login'
    token = post(auth_url, json.dumps(auth))['key']

    label_url = 'http://8.217.95.207:8080/api/labels?job_id=47'
    label_resp = get(label_url, token)

    sublabels = label_resp['results'][0]['sublabels']

    Ids = [ label['id'] for label in sublabels ]

    json_data = create_kps_json_payload(kps_inference('2023101401.jpg'),Ids)

    print(json_data)

    anno_url = 'http://8.217.95.207:8080/api/jobs/47/annotations'
    resp = put(anno_url, json_data, token)
    print(resp)
