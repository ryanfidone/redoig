import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView

from .forms import BookForm, LoanBookForm
from .models import Author, Book, BookInstance, Genre


def index(request):
    """Home page showing a few library statistics."""
    context = {
        "num_books": Book.objects.count(),
        "num_instances": BookInstance.objects.count(),
        "num_instances_available": BookInstance.objects.filter(status="a").count(),
        "num_authors": Author.objects.count(),
        "num_genres": Genre.objects.count(),
    }
    return render(request, "catalog/index.html", context)


class LibrarianRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "catalog/book_list.html"
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "catalog/book_detail.html"


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = "author_list"
    template_name = "catalog/author_list.html"
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "catalog/author_detail.html"


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "catalog/my_books.html"
    context_object_name = "bookinstance_list"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user, status="o"
        ).select_related("book").order_by("due_back")


class AuthorCreate(LibrarianRequiredMixin, CreateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death", "author_image"]
    template_name = "catalog/author_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Author added successfully.")
        return super().form_valid(form)


class AuthorUpdate(LibrarianRequiredMixin, UpdateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death", "author_image"]
    template_name = "catalog/author_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Author updated successfully.")
        return super().form_valid(form)


def author_delete(request, pk):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete authors.")
        return redirect("author_list")
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        if author.books.exists():
            messages.error(request, "This author cannot be deleted because books are associated with them.")
        else:
            author.delete()
            messages.success(request, "Author deleted successfully.")
        return redirect("author_list")
    return render(request, "catalog/author_confirm_delete.html", {"author": author})


class BookCreate(LibrarianRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "catalog/book_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Book added successfully.")
        return response


class BookUpdate(LibrarianRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "catalog/book_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Book updated successfully.")
        return response


def book_delete(request, pk):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete books.")
        return redirect("book_list")
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        if book.instances.exists():
            messages.error(request, "This book cannot be deleted while book copies exist.")
        else:
            book.delete()
            messages.success(request, "Book deleted successfully.")
        return redirect("book_list")
    return render(request, "catalog/book_confirm_delete.html", {"book": book})


class AvailBooksListView(LibrarianRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "catalog/bookinstance_list_available.html"
    context_object_name = "bookinstance_list"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status="a").select_related("book").order_by("book__title")


def loan_book_librarian(request, pk):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "Only librarians can loan books.")
        return redirect("index")

    book_instance = get_object_or_404(BookInstance, pk=pk, status="a")
    if request.method == "POST":
        form = LoanBookForm(request.POST, instance=book_instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.due_back = datetime.date.today() + datetime.timedelta(weeks=4)
            instance.status = "o"
            instance.save()
            messages.success(request, "Book loan recorded.")
            return HttpResponseRedirect(reverse("all_available"))
    else:
        form = LoanBookForm(instance=book_instance, initial={"book_title": book_instance.book.title})
    return render(request, "catalog/loan_book_librarian.html", {"form": form, "book_instance": book_instance})
