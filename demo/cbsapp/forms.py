# -*- coding: utf-8 -*-
from django import forms

from cbsapp.models import Author


class MyForm(forms.Form):
    name = forms.CharField(max_length=128)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        # fields = '__all__'
        fields = ('salutation', 'name', 'email')

    def send_email(self):
        print 'send_email'
