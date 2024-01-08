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
import os
import datetime
from utils.Predictor import Predictor

def create_image_folder(dest_father_dir):
    # 创建存储路径
    img_dir1 = os.path.join(settings.MEDIA_ROOT, dest_father_dir)
    print(dest_father_dir)
    if not os.path.exists(img_dir1):
        os.mkdir(img_dir1)
    img_dir2 = os.path.join(img_dir1, datetime.datetime.now().strftime("%Y"))
    if not os.path.exists(img_dir2):
        os.mkdir(img_dir2)
    img_dir3 = os.path.join(img_dir2, datetime.datetime.now().strftime("%m"))
    if not os.path.exists(img_dir3):
        os.mkdir(img_dir3)
    target_dir = os.path.join(img_dir3, datetime.datetime.now().strftime("%d"))

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    target_dir_relative_path = os.path.relpath(target_dir, settings.MEDIA_ROOT)
    print("target_dir: {} , relative_dir: {} ".format(target_dir, target_dir_relative_path))

    return target_dir, target_dir_relative_path

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
        self.model_name = model_args['model']
        self.model_path = model_args['model_path']
        self.img_height = model_args['img_height']
        self.img_width = model_args['img_width']
        ia.seed(1)


    def kps_predict(self):
        seq = iaa.Sequential([
            iaa.Resize({"height": self.img_height, "width": self.img_width})
        ])
        image_predict = seq(image=self.open_cv_image)

        p = Predictor(self.model_path, image_predict)

        kps_predict = getattr(p, self.model_name)

        kps_predict_tuple = self.kpslist_to_tuple(kps_predict)

        imgoi_array, kpsoi = self.convert_to_original(image_predict, kps_predict_tuple)

        return  imgoi_array, kpsoi

    def convert_to_original(self, tran_img_array: Numpy.ArrayLike, tran_kps: List[Keypoint]):
        seq = iaa.Sequential([
            iaa.Resize({"height": self.open_cv_image.shape[0], "width": self.open_cv_image.shape[1]})
        ])
        imgoi, kpsoi = seq(image=tran_img_array, keypoints=tran_kps)
        print("original keypoints: ",kpsoi)
        return imgoi, kpsoi

    def save_tran_image(self) -> str:
        imgoi_array, kpsoi = self.kps_predict()

        kps_original = KeypointsOnImage(kpsoi, shape=self.open_cv_image.shape)
        image_with_kps = kps_original.draw_on_image(self.open_cv_image, size=15)

        folder, folder_relative = create_image_folder(dest_father_dir='anno_images')
        target_image = os.path.join(folder, self.image_name)
        print("target Image {} ".format(target_image))
        #save image with absolute path
        plt.imsave(target_image, image_with_kps)

        #return image relative path to save in DB
        db_path = os.path.join(folder_relative, self.image_name)

        return db_path


    @staticmethod
    def kpslist_to_tuple(kpsList: List[float]) -> List[Keypoint]:
        converted_keypoints = [list(a) for a in zip(*[iter(kpsList)] * 2)]
        kps = [Keypoint(x=coodination[0], y=coodination[1]) for coodination in converted_keypoints]
        return kps

    @staticmethod
    def kpstuple_to_list(kpsTupleList: List[Keypoint]) -> List:
        ts_kps_row = []
        for i in range(len(kpsTupleList)):
            ts_kps_row.extend([kpsTupleList[i].x, kpsTupleList[i].y])
        return ts_kps_row

    @staticmethod
    def kpstuple_to_couplelist(kpsTupleList: List[Keypoint]) -> List:
        ts_kps_row = []
        for i in range(len(kpsTupleList)):
            ts_kps_row.append([float(kpsTupleList[i].x), float(kpsTupleList[i].y)])
        return ts_kps_row



