from django import forms
from .models import Deck, Card


class DeckCreateForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = [
            'title',
            'image',
            'description'
        ]


class CardCreateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = [
            'title',
            'answer',
            'icon'         
        ]
