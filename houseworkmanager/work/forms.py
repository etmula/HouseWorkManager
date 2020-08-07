from django.forms. import forms

class WorkCreateForm(forms.Form):
    category = forms.CharField(max_length=250)