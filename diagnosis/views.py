from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .forms import DiagnosisForm
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from .models import Diagnosis
from django.contrib import messages
from utils.utils import ImageProcesser
from django.views.generic import ListView
from django.utils import timezone


model_dict = {
    "densenet121": {
        "img_width" : 280,
        "img_height" : 500,
        "model_path" : "D:\/aspine\/densenet121.h5"
    }
}

def DiagnosisView(request):

    template_name = 'diagnosis/image_upload.html'

    if request.method == 'POST':
        form = DiagnosisForm(request.POST, request.FILES)
        context = { 'form': form }

        if form.is_valid():
            img = form.cleaned_data.get("img")
            type = form.cleaned_data.get("type")
            obj = Diagnosis.objects.create(
                img=img,
                type=type
            )
            try:
                annotated_image = ImageProcesser(image_path=obj.img.path, model_args=model_dict['densenet121'])
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

class JoblistView(ListView):

    template_name = 'diagnosis/job_list.html'
    model = Diagnosis
    paginate_by = 5  # if pagination is desired

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

