from django import forms


class URLForm(forms.Form):
    form = forms.URLField(label='URL',max_length=100,)

