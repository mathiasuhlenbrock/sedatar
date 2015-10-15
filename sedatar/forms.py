from django import forms

class SearchForm(forms.Form):
    question = forms.CharField(label='', max_length = 100)
    answer   = "Answer"
