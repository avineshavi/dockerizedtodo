from django import forms



class CreateForm(forms.Form):
    repeat_choices = (
        ( 'daily', 'daily' ),
        ( 'weekly', 'weekly' ),
        ( 'monthly', 'monthly' ),
    )
    name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Task Name'}), max_length=200,label="Task Name :")
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Here can be Description', 'rows' : 5, 'cols' : 10}),max_length=200,label="Description :")
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local','class':'form-control'}),label="Date & Time :")
    repeat = forms.ChoiceField(widget = forms.Select(attrs={'class':'form-control'}), choices=repeat_choices, required=True, label="Repeat :")


class EmailForm(forms.Form):
    email = forms.EmailField()