from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Buscar productos', max_length=100)
    search_type = forms.ChoiceField(choices=[('all', 'Todos'), ('motorcycles', 'Motocicletas'), ('parts', 'Partes'), ('manufacturers', 'Fabricantes')],
                                   initial='all', widget=forms.Select(attrs={'class': 'form-control'}))
    min_price = forms.DecimalField(
        label='Precio mínimo',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    max_price = forms.DecimalField(
        label='Precio máximo',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    score = forms.IntegerField(
        label='Puntuación',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )