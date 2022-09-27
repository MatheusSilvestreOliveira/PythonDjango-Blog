from django.forms import ModelForm
from .models import Comments
import requests


class FormComment(ModelForm):
    def clean(self):
        raw_data = self.data
        recaptcha_response = raw_data.get('g-recaptcha-response')
        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': '6Lc61DYiAAAAABOeMLfOpUcSwwO3T44zVlP_t29f',
                'response': recaptcha_response
            }
        )
        recaptcha_result = recaptcha_request.json()
        if not recaptcha_result.get('success'):
            self.add_error('comment', 'reCAPTCHA failed, try again.')

        cleaned_data = self.cleaned_data
        name = cleaned_data.get('comment_name')
        email = cleaned_data.get('comment_email')
        comment = cleaned_data.get('comment')

        if len(name) < 4:
            self.add_error('comment_name', 'Name length must be longer than 4 characters.')

        if not comment and recaptcha_result.get('success'):
            self.add_error('comment', 'Comment is required to submit.')

    class Meta:
        model = Comments
        fields = ('comment_name', 'comment_email', 'comment',)
