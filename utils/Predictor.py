from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import torch
from imgaug.augmentables.kps import Keypoint, KeypointsOnImage
import numpy as np
from PIL import Image
from imgaug.augmentables.kps import Keypoint, KeypointsOnImage
from keras.models import load_model
from django.conf import settings
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "aiapi.settings"
from imgaug import augmenters as iaa
import imgaug as ia
from typing import List,Dict
import numpy.typing as Numpy


class Predictor:

    def __init__(self,model_path, image):
        self.model_path = model_path
        self.image = image
    @property
    def Pivles_Densenet121(self) -> List[float]:
        model = load_model(self.model_path)
        kps_group = model.predict(np.stack([self.image]))
        kps_predict = kps_group.tolist()[0]

        return kps_predict

    @property
    def SelfAssessAP10_Yolov8(self) -> List[float]:
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        model = YOLO(self.model_path)
        model.to(device)
        results = model(self.image, conf=0.7)

        bboxes_keypoints = results[0].keypoints.data.cpu().numpy().tolist()

        print(bboxes_keypoints)
        indices_to_access = [2,1,6,5,12,11,14,13,16,15]
        kps_predict = []
        for kp in bboxes_keypoints:
            for idx,el in enumerate(kp):
                if idx in indices_to_access:
                    kps_predict.extend(el[0:2])
        return kps_predict

    @property
    def SelfAssessLT5_Yolov8(self) -> List[float]:
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        model = YOLO(self.model_path)
        model.to(device)
        results = model(self.image, conf=0.7)

        bboxes_keypoints = results[0].keypoints.data.cpu().numpy().tolist()

        print(bboxes_keypoints)
        indices_to_access = [4,6,12,14,16]
        kps_predict = []
        for kp in bboxes_keypoints:
            for idx,el in enumerate(kp):
                if idx in indices_to_access:
                    kps_predict.extend(el[0:2])
        return kps_predict
