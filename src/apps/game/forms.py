from django import forms

from game.models import Team

class RennerForm(forms.Form):
    naam = forms.CharField()
    nummer = forms.CharField()
    team = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label="Kies team")
