from django import forms


class ObjectForm(forms.Form):
    object = forms.CharField(id='object', max_length=100)
