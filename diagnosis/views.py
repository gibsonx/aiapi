from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .forms import DiagnosisForm, JobDiagnosisForm
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from .models import Diagnosis
from django.contrib import messages
from utils.ImageProcesser import ImageProcesser
from django.views.generic import ListView
from django.conf import settings
from utils.CvatHelper import CvatJobHelper
from typing import List,Dict,Tuple
from diagnosis.tasks import *

def DiagnosisView(request):

    template_name = 'diagnosis/image_upload.html'

    if request.method == 'POST':
        form = DiagnosisForm(request.POST, request.FILES)
        context = { 'form': form }

        if form.is_valid():
            img = form.cleaned_data.get("img")
            diag_type = form.cleaned_data.get("type")
            obj = Diagnosis.objects.create(
                img=img,
                type=diag_type
            )
            print("current diag nose type is %s " % diag_type)
            if diag_type == "1":
                annotated_image = ImageProcesser(image_path=obj.img.path, model_args=settings.MODEL_DICT['SelfAssessAP10'])
            elif diag_type == "2":
                annotated_image = ImageProcesser(image_path=obj.img.path, model_args=settings.MODEL_DICT['Pivles'])
            anno_path = annotated_image.save_tran_image()

            if anno_path:
                try:

                    obj.anno_img = annotated_image.save_tran_image()
                    obj.save()
                except Exception as e:
                    print(e)

            messages.add_message(request, messages.INFO, "Job Id: {} 提交成功, 请去历史中等待查看".format(obj.id))
            return HttpResponseRedirect("/diag/")
    else:
       form = DiagnosisForm()
       context = {'form': form }

    return render(request, template_name, context)


def send_annotation(DiagId: int) -> Tuple[bool, str]:
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
    obj = Diagnosis.objects.get(id=DiagId)
    job = CvatJobHelper(obj.jobid)
    # Retrieve the target image and its relative path
    target_image, target_image_relative = job.get_job_image()

    # Depending on the diagnosis type of the Diagnosis object, create an ImageProcesser instance with the appropriate model arguments
    if obj.type == 1:
        annotated_image = ImageProcesser(image_path=target_image, model_args=settings.MODEL_DICT['SelfAssessAP10'])
    elif obj.type == 2:
        annotated_image = ImageProcesser(image_path=target_image, model_args=settings.MODEL_DICT['SelfAssessLT5'])
    elif obj.type == 3:
        annotated_image = ImageProcesser(image_path=target_image, model_args=settings.MODEL_DICT['Pivles'])
    else:
        return False, "failed"

    # Predict keypoints on the image and convert them into a list of tuples
    imgoi_array, kpsoi = annotated_image.kps_predict()
    kps = annotated_image.kpstuple_to_couplelist(kpsoi)

    print("mark annotations on cvat with payload", job.post_anno(kps))
    anno_path = annotated_image.save_tran_image()
    # If the saving is successful, update the Diagnosis object with the relative path of the target image and the path of the annotated image
    if anno_path:
        obj.img=target_image_relative
        obj.anno_img = anno_path
        try:
            obj.save()
            return True, "success"
        except Exception as e:
            print(e)
            return False, e


def JobDiagnosisView(request):
    template_name = 'diagnosis/job_submit.html'

    if request.method == 'POST':
        form = JobDiagnosisForm(request.POST)
        context = { 'form': form }

        if form.is_valid():
            jobid = form.cleaned_data.get("jobid")
            diag_type = form.cleaned_data.get("type")

            obj = Diagnosis.objects.create(
                jobid=jobid,
                type=diag_type
            )

            # synchronous execution
            status, async_task = send_annotation(DiagId=obj.id)

            # asynchronous exeuction
            # async_task = send_annotation.delay(DiagId=obj.id)

            if status:
                messages.add_message(request, messages.INFO, "Job Id: {} 提交成功, 请去历史中等待查看".format(obj.id))
            return HttpResponseRedirect("/diag/jobsubmit/")
    else:
       form = JobDiagnosisForm()
       context = {'form': form }

    return render(request, template_name, context)


class JoblistView(ListView):

    template_name = 'diagnosis/job_list.html'
    model = Diagnosis
    paginate_by = 5  # if pagination is desired

    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        all_msgs = {}
        context = super().get_context_data(**kwargs)
        context['all_msgs'] = all_msgs
        page = context.get('page_obj')
        paginator = context.get('paginator')

        context_data = self.get_page(paginator, page)
        context.update(context_data)

        return context

    def get_page(self,paginator,page,page_offset=2):
        left_more_page = False
        right_more_page = False
        #获取当前页码
        current_num = page.number
        if current_num <= page_offset+2:
            left_range = range(1,current_num)
        else:
            left_more_page = True
            left_range = range(current_num-page_offset,current_num)
        if current_num >= paginator.num_pages-page_offset-1:
            right_range = range(current_num+1,paginator.num_pages+1)
        else:
            right_more_page = True
            right_range = range(current_num+1,current_num+page_offset+1)
        return {
            'left_range':left_range,
            'right_range':right_range,
            'left_more_page':left_more_page,
            'right_more_page':right_more_page,
        }

