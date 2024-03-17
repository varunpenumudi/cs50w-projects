from django import forms 

class NewSearchForm(forms.Form):
    query = forms.CharField(label="",widget=forms.TextInput( attrs= {
        'placeholder':'Search Encyclopedia',
        'class':'search'
    }) )

class NewEntryForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput( attrs= {
        'placeholder':'Enter Title',
        'class':'title_field'
    }))
    contents = forms.CharField(label="", widget=forms.Textarea(attrs={
        'placeholder':'Enter Content in Markdown Format',
        'rows':5,
        'cols':20
    }))

class NewEditForm(forms.Form):
    contents = forms.CharField(label="", widget=forms.Textarea(attrs={
    }))