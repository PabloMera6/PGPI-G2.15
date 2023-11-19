from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Buscar productos', max_length=100)
    search_type = forms.ChoiceField(choices=[('all', 'Todos'), ('motorcycles', 'Motocicletas'), ('parts', 'Partes'), ('manufacturers', 'Fabricantes')],
                                   initial='all', widget=forms.Select(attrs={'class': 'form-control'}))
