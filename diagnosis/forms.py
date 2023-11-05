from django.forms import ModelForm,Form,fields,widgets
from diagnosis.models import Diagnosis

class DiagnosisForm(ModelForm):
    type = fields.ChoiceField(
        label="诊断类型:",
        required=True,
        initial=1,  # 默认选择1号
        choices=((1, "自我诊断"), (2, "骨盆"),),
        widget=widgets.Select
    )

    class Meta:
        model = Diagnosis
        fields = ['img','type']

