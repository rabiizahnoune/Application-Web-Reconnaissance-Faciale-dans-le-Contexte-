# forms.py

from django import forms

class FacialRecognitionForm(forms.Form):
    label = forms.CharField(max_length=100)
    
    captured_image = forms.CharField(widget=forms.HiddenInput(), required=False) 

class SelectClassForm(forms.Form):
    CHOICES = [('MIP', 'MIP'), ('BCG', 'BCG')]  # Ajoutez d'autres classes au besoin
    CHOICES1=[("S1","S1"),("S2","S2")]
    selected_class = forms.ChoiceField(choices=CHOICES, label='Select a class')
    selected_semester = forms.ChoiceField(choices=CHOICES1, label='selected_semester')
# forms.py
from django import forms

class ImporterRepertoireForm(forms.Form):
    repertoire = forms.FileField(label='Sélectionnez le répertoire à importer', help_text='Format ZIP uniquement')
    CHOICES = [('MIP', 'MIP'), ('BCG', 'BCG')]  # Ajoutez d'autres classes au besoin
    CHOICES1=[("S1","S1"),("S2","S2")]
    selected_class = forms.ChoiceField(choices=CHOICES, label='Select a class')
    selected_semester = forms.ChoiceField(choices=CHOICES1, label='selected_semester')





