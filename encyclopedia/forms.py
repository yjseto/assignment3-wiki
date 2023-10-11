from django import forms


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    newentry = forms.CharField(widget=forms.Textarea, label="New Entry")
    
