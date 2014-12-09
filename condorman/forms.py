from django import forms
from condorman.models import CondorUser, PrioFactor
from condorman.util import getUserList
from django.forms import forms, ModelForm
from django.contrib.admin import widgets

class PrioFactorForm(ModelForm):
    class Meta:
        model = PrioFactor

    def __init__(self, *args, **kwargs):
        super(PrioFactorForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = widgets.AdminDateWidget()
        self.fields['end_date'].widget = widgets.AdminDateWidget()
        self.fields['user'].queryset = getUserList().order_by('username')

    def clean(self):
        cleaned_data = super(PrioFactorForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if (end_date <= start_date):
            raise forms.ValidationError("end_date must be "
                                        "later than start_date")

        return cleaned_data
