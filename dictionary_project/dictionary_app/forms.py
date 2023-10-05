from django.forms import ModelForm
from .models import Dict

class AddWordForm(ModelForm):
    class Meta:
        model = Dict
        fields = ['word', 'translation', 'prompt']
