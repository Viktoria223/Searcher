from django import forms


class SearchForm(forms.Form):
    word = forms.CharField()

    def clean_word(self):
        cleaned_data = super(SearchForm, self).clean()
        word = cleaned_data.get("word")
        return word
