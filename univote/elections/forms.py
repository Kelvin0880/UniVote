
from django import forms
from .models import Election, Candidate, Vote
from django.utils import timezone

class ElectionForm(forms.ModelForm):
    """Formulario para crear y editar elecciones."""
    class Meta:
        model = Election
        fields = ['title', 'description', 'start_date', 'end_date', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")
            
            if start_date < timezone.now() and self.instance.pk is None:
                raise forms.ValidationError("No puedes crear una elección con una fecha de inicio en el pasado.")
        
        return cleaned_data

class CandidateForm(forms.ModelForm):
    """Formulario para crear y editar candidatos."""
    class Meta:
        model = Candidate
        fields = ['election', 'name', 'photo', 'position', 'bio']
        widgets = {
            'election': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class VoteForm(forms.Form):
    """Formulario para votar por un candidato."""
    candidate = forms.ModelChoiceField(
        queryset=Candidate.objects.none(),
        empty_label=None,
        widget=forms.RadioSelect
    )
    
    def __init__(self, election, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['candidate'].queryset = Candidate.objects.filter(election=election)