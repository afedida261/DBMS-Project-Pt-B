from django import forms
from .models import Applications


class ApplicationForm(forms.Form):
    aName = forms.CharField(label='App Name', max_length=100)
    aCategory = forms.ChoiceField(label='Category', widget=forms.Select(attrs={'size': 5}))
    aSize = forms.IntegerField(
        label='App Size',
        min_value=100,
        max_value=200,
        help_text='Enter a size between 100 and 200 MB.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the category choices with distinct categories from the Applications table.
        categories = Applications.objects.values_list('acategory', flat=True).distinct()
        choices = [(cat, cat) for cat in categories]
        self.fields['aCategory'].choices = choices

    def clean_aName(self):
        name = self.cleaned_data['aName']
        if Applications.objects.filter(aname=name).exists():
            raise forms.ValidationError("An application with this name already exists.")
        return name


class InstallApplicationForm(forms.Form):
    # A choice field that will display only apps with isinstalled = 0
    app = forms.ChoiceField(label='', widget=forms.Select(attrs={'size': 5}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Query only apps that are not installed (isinstalled = 0) and sort by name.
        available_apps = Applications.objects.filter(isinstalled=0).order_by('aname')
        choices = [(app.aname, app.aname) for app in available_apps]
        self.fields['app'].choices = choices


class RemoveApplicationForm(forms.Form):
    app = forms.ChoiceField(label='', widget=forms.Select(attrs={'size': 5}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        installed_apps = Applications.objects.filter(isinstalled=1).order_by('aname')
        choices = [(app.aname, app.aname) for app in installed_apps]
        self.fields['app'].choices = choices