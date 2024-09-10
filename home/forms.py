from django import forms

from .models import LostItem, FoundItem, Hub


class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        exclude = ['sub_date', 'user', 'location']
        # widget sources:
        # https://medium.com/swlh/how-to-style-your-django-forms-7e8463aae4fa
        # https://docs.djangoproject.com/en/4.2/ref/forms/widgets/
        widgets = {
            'category': forms.Select(attrs={
                'class': "form-select",
                'style': 'width: 100%;',
            }),
            'description': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'width: 100%;',
                'placeholder': 'Enter description here'
            }),
            'reward': forms.NumberInput(attrs={
                'class': "form-control",
                'style': 'width: 100%;',
                'aria-describedby': 'addon-wrapping'
            }),
        }

    def clean(self):
        data = self.cleaned_data
        return data

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        # exclude = ['found_date', 'user', 'location']
        fields = ('category', 'item_description', 'hub')
        # widget sources same as above
        widgets = {
            'category': forms.Select(attrs={
                'class': "form-select",
                'style': 'width: 100%;',
            }),
            'item_description': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'width: 100%;',
                'placeholder': 'Enter description here'
            }),
            'hub': forms.Select(attrs={
                'class': "form-select",
                'style': 'width: 100%;'
            }),
        }

    # filter approved hub source (answer from KenWhitesell):
    # https://forum.djangoproject.com/t/how-to-filter-the-choices-in-forms-select-widget/19974/4
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hub'].queryset = Hub.objects.filter(approved=True)
        self.fields['hub'].required = False

    def clean(self):
        data = self.cleaned_data
        return data


class HubForm(forms.ModelForm):
    class Meta:
        model = Hub
        exclude = ['location', 'approved']
        # widget sources same as above
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'width: 100%;',
                'placeholder': 'Enter name here'
            }),
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'width: 100%;',
                'placeholder': 'Enter description here'
            }),
        }


    def clean(self):
        data = self.cleaned_data
        return data

