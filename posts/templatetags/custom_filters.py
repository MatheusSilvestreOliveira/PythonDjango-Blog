from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter(name='plural_comments')
@stringfilter
def plural_comments(n_comments):
    try:
        n_comments = int(n_comments)
        if n_comments == 0:
            return f'No comments'
        elif n_comments == 1:
            return f'{n_comments} comment'
        else:
            return f'{n_comments} comments'
    except:
        return f'{n_comments} comment(s)'
