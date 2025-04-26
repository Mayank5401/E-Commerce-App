# forms.py
from django import forms

class RatingForm(forms.Form):
    score = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        label='Rating',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    review = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )

