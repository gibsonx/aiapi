from django.forms import ModelForm,Form,fields,widgets
from diagnosis.models import Diagnosis


diagnosis_choices = ((1, "自我诊断AP11"), (2, "自我诊断LT5"), (3, "骨盆AP16"),)

class DiagnosisForm(ModelForm):
    type = fields.ChoiceField(
        label="诊断类型:",
        required=True,
        initial=1,  # 默认选择1号
        choices=diagnosis_choices,
        widget=widgets.Select
    )

    class Meta:
        model = Diagnosis
        fields = ['img','type']


class JobDiagnosisForm(ModelForm):
    type = fields.ChoiceField(
        label="诊断类型:",
        required=True,
        initial=1,  # 默认选择1号
        choices=diagnosis_choices,
        widget=widgets.Select
    )

    class Meta:
        model = Diagnosis
        fields = ['jobid','type']

