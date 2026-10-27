from django import forms
from .models import Book, BookInstance, Genre


class LoanBookForm(forms.ModelForm):
    book_title = forms.CharField(label="Book", disabled=True, required=False)

    class Meta:
        model = BookInstance
        fields = ("book_title", "borrower")


class BookForm(forms.ModelForm):
    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Book
        fields = ("title", "author", "summary", "isbn", "genre", "book_image")
