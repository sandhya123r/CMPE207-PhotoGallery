from django import forms


class AlbumForm(forms.Form):
    name = forms.CharField(label='Album name', max_length=100)


class UploadForm(forms.Form):
    docfile = forms.ImageField(
        label='Select an Image',
        help_text=''
    )