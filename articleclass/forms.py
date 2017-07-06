from django import forms


# フォーム
class URLForm(forms.Form):
    form = forms.URLField(label='URL', max_length=100,)
