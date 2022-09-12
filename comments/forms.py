from django.forms import ModelForm
from .models import Comments


class FormComment(ModelForm):
    def clean(self):
        data = self.cleaned_data
        name = data.get('comment_name')
        email = data.get('comment_email')
        comment = data.get('comment')

        if len(name) < 4:
            self.add_error('comment_name', 'Name length must be longer than 4 characters.')

        if not comment:
            self.add_error('comment', 'Comment is required to submit.')

    class Meta:
        model = Comments
        fields = ('comment_name', 'comment_email', 'comment',)
