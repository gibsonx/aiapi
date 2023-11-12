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
    def DenseNet(self):
        model = load_model(self.model_path)
        kps_group = model.predict(np.stack([self.image]))
        kps_predict = kps_group.tolist()[0]

        return kps_predict

    @property
    def Yolo8(self):
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        model = YOLO(self.model_path)
        model.to(device)
        results = model(self.image, conf=0.7)

        bboxes_keypoints = results[0].keypoints.data.cpu().numpy().tolist()

        kps_predict = []
        for kp in bboxes_keypoints:
            for el in kp:
                kps_predict.extend(el[0:2])

        return kps_predict

        # kps_predict_tuple = self.kpslist_to_tuple(kps_predict)


# # 有 GPU 就用 GPU，没有就用 CPU
# device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# model = YOLO('D:\/aspine\/yolov8x-pose-p6.pt')
#
# def kpslist_to_tuple(kpsList):
#     converted_keypoints = [list(a) for a in zip(*[iter(kpsList)] * 2)]
#     kps = [Keypoint(x=coodination[0], y=coodination[1]) for coodination in converted_keypoints]
#     return kps
#
# source = r"C:\Users\Administrator\PycharmProjects\aiapi\media\images\doctor.jpg"
#
# open_cv_image = np.array(Image.open(source))
# # 切换计算设备
# model.to(device)
#
# ##预测  传入图像、视频、摄像头ID（对应命令行的 source 参数）
# # img_path = source
# results = model(source, conf=0.7)
#
# num_bbox = len(results[0].boxes.cls)
# print('预测出 {} 个框'.format(num_bbox))
# # 转成整数的 numpy array
# bboxes_xyxy = results[0].boxes.xyxy.cpu().numpy().astype('uint32')
# print("bboxes_xyxy:",bboxes_xyxy)
# ## 解析关键点检测预测结果
#
# bboxes_keypoints = results[0].keypoints.data.cpu().numpy().tolist()
#
# print(bboxes_keypoints)

# keypoints_original = [[list(a) for a in zip(*[iter(bboxes_keypoints[0])]*3)]]
#
# print(keypoints_original)

# converted_keypoints = [ el[0:2] for kp in bboxes_keypoints for el in kp ]
# print(converted_keypoints)
#
# kps_row = []
# for kp in bboxes_keypoints:
#     for el in kp:
#         kps_row.extend(el[0:2])
#
# print(len(kps_row))
#
# keypoint = kpslist_to_tuple(kps_row)
# # #
#
# kpsoi = KeypointsOnImage(kpslist_to_tuple(kps_row), shape=open_cv_image.shape)
#
# image_with_kps = kpsoi.draw_on_image(open_cv_image, size=15)
#
# plt.imshow(image_with_kps)
# plt.show()
