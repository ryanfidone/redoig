import uuid
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    """A category of book, for example fantasy or science fiction."""
    name = models.CharField(max_length=200, unique=True, help_text="Enter a book genre.")

    class Meta:
        ordering = ["name"]
        permissions = []

    def __str__(self):
        return self.name


class Author(models.Model):
    """A person who wrote a book."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)
    author_image = models.ImageField(upload_to="images/authors/", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        permissions = [
            ("create_author", "Can create author"),
        ]

    def get_absolute_url(self):
        return reverse("author_detail", args=[str(self.pk)])

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Book(models.Model):
    """A title, which can have one or more physical copies."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.RESTRICT, null=True, related_name="books")
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book.")
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        unique=True,
        help_text="13-character ISBN, without hyphens.",
    )
    genre = models.ManyToManyField(Genre, help_text="Select one or more genres.")
    book_image = models.ImageField(upload_to="images/books/", null=True, blank=True)

    class Meta:
        ordering = ["title"]
        permissions = [
            ("create_book", "Can create book"),
        ]

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.pk)])

    def __str__(self):
        return self.title

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = "Genre"


class BookInstance(models.Model):
    """A particular physical copy of a book."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this copy.")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True, related_name="instances")
    imprint = models.CharField(max_length=200, blank=True)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="m", help_text="Book availability")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="borrowed_copies")

    class Meta:
        ordering = ["due_back", "book__title"]

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    def __str__(self):
        return f"{self.id} ({self.book.title if self.book else 'No book'})"
