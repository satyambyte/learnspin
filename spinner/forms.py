from django import forms
from .models import LearningList , LearningItem , SpinResult

class LearningListForm(forms.ModelForm):
    class Meta:
        model = LearningList
        fields = ['name' , 'category']

class LearningItemForm(forms.ModelForm):
    class Meta:
        model = LearningItem
        fields = ['title' , 'url' , 'weight']

class OutcomeForm(forms.ModelForm):
    class Meta:
        model = SpinResult
        fields = ['outcome' , 'skip_reason']


