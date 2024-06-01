from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=64, label="",
                              widget=forms.Textarea(attrs={
                                  'class':'form-control ml-2', 'placeholder':'Comment',
                                  'style':'resize: none;' ,'rows':4,'cols':180}
                              )
                    )

class ListingCreationForm(forms.Form):
    title = forms.CharField(max_length=64, label="Title*", 
                                   widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title for Listing'})
                    )
    description = forms.CharField(label="Description*", 
                                  widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter Description', 'rows':3}),
                    )
    starting_bid = forms.FloatField(label="Starting Bid*", 
                                    widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Starting Bid Amount'})
                    )
    image_url = forms.URLField(max_length=300, label="Image URL", required=False,
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'URL For Image'})
                )
    category = forms.CharField(max_length=64, label="Category", required=False,
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Category'})
                )


