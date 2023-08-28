from django import forms
from .models import Comment, Contact
from django.contrib.auth import authenticate


class CommentForm(forms.ModelForm):

    comment_body = forms.CharField(widget = forms.Textarea(attrs = {
        'class': 'form-control',
        'placeholder': 'Rəy Əlavə Et',
        'label': 'Rey',
        'rows': 4,
        
    }))


    class Meta:
        model = Comment
        fields = ('comment_body',)
        # widgets = {
        #     'comment_body': forms.Textarea(attrs = {'class': 'form-control'})
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs.update({
    #             'class' : 'form-control',
    #             'placeholder' : f'{self.fields[field].label}'
    #         })


class ProductSearchForm(forms.Form):
    search_query = forms.CharField(label='Search by Code', max_length=50)


class ContatForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'subject', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : 'form-control',
                'placeholder' : f'{self.fields[field].label}'
            })

    def clean(self):
        attrs = self.cleaned_data

        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        email = attrs.get('email')
        subject = attrs.get('subject')
        description = attrs.get('description')

        
        if first_name == '':
            raise forms.ValidationError('Ad boş qoyula bilməz!')
        
        
        return attrs