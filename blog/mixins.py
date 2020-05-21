from django import forms
from django.core.exceptions import FieldError, ValidationError


class FormMixin(forms.ModelForm):
    def clean_slug(self, *args, **kwargs):
        slug = self.cleaned_data['slug'].lower()    # TO DO переписать на .get()
        # if not slug:
        #     raise FieldError('Slug can`t be a None')

        if slug == 'create':
            raise ValidationError('Slug can`t be "create"')
        if self.Meta.model.objects.filter(slug__iexact=slug).count():
            raise ValidationError(f'Slug "{slug}" is already exists, try another slug')
        
        return slug