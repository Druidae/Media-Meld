from django import forms


class MediaMeldForms(forms.Form):
    title = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Your Video Link'})
    )
