import matplotlib.pyplot as plt
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

class ImageProcesser:

    def __init__(self, image_path: str, model_args: Dict):
        """
        :param image_path: original image to annotate
        :param model_path: ML model path
        :param img_height: target height after image shape transform
        :param img_width: target width after image shape transform
        """
        self.image_path = image_path
        self.image_name = self.image_path.split('\\')[-1]
        self.open_cv_image = np.array(Image.open(self.image_path))
        self.model_path = model_args['model_path']
        self.img_height = model_args['img_height']
        self.img_width = model_args['img_width']
        ia.seed(1)

    def kps_predict(self) :
        seq = iaa.Sequential([
            iaa.Resize({"height": self.img_height, "width": self.img_width})
        ])
        image_predict = seq(image=self.open_cv_image)
        model = load_model(self.model_path)
        kps_group = model.predict(np.stack([image_predict]))
        kps_predict = kps_group.tolist()[0]
        kps_predict_tuple = self.kpslist_to_tuple(kps_predict)
        imgoi_array, kpsoi = self.convert_to_original(image_predict, kps_predict_tuple)

        return  imgoi_array, kpsoi

    def convert_to_original(self, tran_img_array: Numpy.ArrayLike, tran_kps: List[Keypoint]):
        seq = iaa.Sequential([
            iaa.Resize({"height": self.open_cv_image.shape[0], "width": self.open_cv_image.shape[1]})
        ])
        imgoi, kpsoi = seq(image=tran_img_array, keypoints=tran_kps)
        return imgoi, kpsoi

    def save_tran_image(self) -> str:
        imgoi_array, kpsoi = self.kps_predict()
        kps_original = KeypointsOnImage(kpsoi, shape=self.open_cv_image.shape)
        image_with_kps = kps_original.draw_on_image(self.open_cv_image, size=5)

        target_folder = os.path.join(settings.MEDIA_ROOT, 'anno_images')
        target_image = os.path.join(target_folder, self.image_name)

        plt.imsave(target_image, image_with_kps)
        db_path = os.path.join('anno_images', self.image_name)

        return db_path

    def kpslist_to_tuple(self, kpsList: List[float]) -> List[Keypoint]:
        converted_keypoints = [list(a) for a in zip(*[iter(kpsList)] * 2)]
        kps = [Keypoint(x=coodination[0], y=coodination[1]) for coodination in converted_keypoints]
        return kps

    def kpstuple_to_list(self, kpsTupleList: List[Keypoint]) -> List:
        ts_kps_row = []
        for i in range(len(kpsTupleList)):
            ts_kps_row.extend([kpsTupleList[i].x, kpsTupleList[i].y])
        return ts_kps_row


# def save_tran_image(image_path, model_path=None, img_height=500, img_width=280):
#
#     open_cv_image = np.array(Image.open(image_path))
#
#     ia.seed(1)
#
#     seq = iaa.Sequential([
#         iaa.Resize({"height": img_height, "width": img_width})
#     ])
#
#     image_predict = seq(image=open_cv_image)
#
#     model = load_model(model_path)
#     picture = np.stack([image_predict])
#     kps_group = model.predict(picture)
#     kps_predict = kps_group.tolist()[0]
#
#     kps_predict_tuple = kpslist_to_tuple(kps_predict)
#
#     image_original, kpsoi_original = convert_original_size(image_predict, kps_predict_tuple)
#
#     kpsoi = KeypointsOnImage(kpsoi_original, shape=image_original.shape)
#
#     image_with_kps = kpsoi.draw_on_image(image_original, size=5)
#
#     TargetFolder = os.path.join(settings.MEDIA_ROOT, 'anno_images')
#
#     image_name = image_path.split('\\')[-1]
#
#     target_image = os.path.join(TargetFolder,image_name)
#
#     plt.imsave(target_image,image_with_kps)
#
#     return  os.path.join('anno_images',image_name)


# def kpslist_to_tuple(kpsList: List) -> List[Keypoint]:
#   converted_keypoints = [list(a) for a in zip(*[iter(kpsList)]*2)]
#   kps = [Keypoint(x=coodination[0], y=coodination[1]) for coodination in converted_keypoints]
#   return kps
#
# def kpstuple_to_list(kpsTupleList):
#   ts_kps_row = []
#   for i in range(len(kpsTupleList)):
#       ts_kps_row.extend([kpsTupleList[i].x,kpsTupleList[i].y])
#   return ts_kps_row
#
#
# def convert_original_size(image_array, kps):
#     seq = iaa.Sequential([
#         iaa.Resize({"height": image_array.shape[0], "width": image_array.shape[1]})
#     ])
#     image_original, kpsoi_original = seq(image=image_array, keypoints=kps)
#     print(kpsoi_original)
#     # image_with_kps = kpsoi_original.draw_on_image(image_original, size=15)
#
#     return image_original, kpsoi_original


