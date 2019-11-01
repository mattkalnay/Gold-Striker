from django import forms
from django.core.exceptions import ValidationError
import re

def validateLetter(value):
    passableCharacter =  re.compile(r'^[a-zA-Z]$')
    print(passableCharacter)
    if passableCharacter.match(value) == None:
        raise ValidationError(
    'Guess Must Be a Letter Between A-Z'
    )

 
class GuessForm(forms.Form):
    letter = forms.CharField(label='', max_length=1, validators = [validateLetter])


DIFFICULTY_CHOICES = [
    ('easy', 'Easy (1000 Points)'),
    ('medium', 'Medium (2000 Points)'),
    ('hard', 'Hard (3000 Points)'),
    ('crazy', 'Crazy (4000 Points)')]

class LoadingForm(forms.Form):
    difficulty = forms.CharField(label='', widget=forms.RadioSelect(choices=DIFFICULTY_CHOICES, attrs={'id':'difficultyLevel'}))

    a = forms.IntegerField(label='Position A', min_value=1, widget=forms.TextInput(attrs={'id':'positionA'}))
    b = forms.IntegerField(label='Position B', min_value=1, widget=forms.TextInput(attrs={'id':'positionB'}))
    c = forms.IntegerField(label='Position C', min_value=1, widget=forms.TextInput(attrs={'id':'positionC'}))
    d = forms.IntegerField(label='Position D', min_value=1, widget=forms.TextInput(attrs={'id':'positionD'}))
    e = forms.IntegerField(label='Position E', min_value=1, widget=forms.TextInput(attrs={'id':'positionE'}))
    f = forms.IntegerField(label='Position F', min_value=1, widget=forms.TextInput(attrs={'id':'positionF', 'readonly':True}))



