from django import forms
#from .models import Profile
from main.models import Report

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['avatar']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'other_reason']

    other_reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'style': 'width: 100%;'}))

    def clean(self):
        cleaned_data = super().clean()
        reason = cleaned_data.get('reason')
        other_reason = cleaned_data.get('other_reason')

        if reason == 'Other' and not other_reason:
            self.add_error('other_reason', 'Будь ласка, вкажіть іншу причину.')

        return cleaned_data