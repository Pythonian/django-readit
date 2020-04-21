from django import forms
from .models import Book


class ReviewForm(forms.Form):
    """ Form for reviewing a book. """

    is_favourite = forms.BooleanField(
        label='Favourite?'
        help_text='In your top 20 books of all',
        required=False,
    )
    review = forms.CharField(
        widget=forms.Textarea,
        min_length=300,
        error_messages={
            'required': 'Please enter your review',
            'min_length': 'Please write at least 300 characters. \
                            You have written %(show_vars) characters.'
        }
    )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'review', 'reviewed_by']

    def clean(self):
        super(BookForm, self).clean()

        try:
            title = self.cleaned_data.get('title')
            authors = self.cleaned_data.get('authors')
            book = Book.objects.get(title=title, authors=authors)

            raise forms.ValidationError(
                'The book {} by {} already exists'.format(
                    title, book.list_authors()),
                code='bookexists'
            )
        except Book.DoesNotExist:
            return self.cleaned_data
