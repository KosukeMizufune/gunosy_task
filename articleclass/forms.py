from django import forms


# 入力フォーム
class URLForm(forms.Form):
    form = forms.URLField(label='URL', max_length=100,)
