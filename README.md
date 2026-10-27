# Local Library — complete starter project

This project combines the standard Django Local Library foundation with the features specified in the uploaded ISQA 3900 Assignment 2 tutorial:
- books, authors, genres, and individual book copies
- login/logout and member registration
- a LibraryMember group (created automatically by the setup command)
- "My Books" for a logged-in borrower
- librarian-only author and book create/edit/delete pages
- author and book images
- librarian view of available copies and a loan form (four-week due date)
- Bootstrap-based templates and custom CSS
- WhiteNoise static-file support

## 1. Create a virtual environment and install packages

Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Create the database

```bash
python manage.py makemigrations catalog
python manage.py migrate
python manage.py setup_library
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and the admin at http://127.0.0.1:8000/admin/.

The `setup_library` command creates the `LibraryMember` group with view-only permissions for catalog models. For a real deployment, set a strong `SECRET_KEY`, `DEBUG=False`, and `ALLOWED_HOSTS` via environment variables.

## 3. Add sample data

Log in to `/admin/` and create at least:
- 2 authors
- 2 genres
- 2 books, assigning authors and genres
- 2 book instances with status `Available`
- one ordinary user assigned to `LibraryMember`

Or use the librarian pages to add/edit authors and books. Image uploads are optional.

## 4. Useful URLs

- `/` home
- `/catalog/book_list/` all books
- `/catalog/author_list/` all authors
- `/accounts/login/` login
- `/accounts/logout/` logout (POST)
- `/register/` sign up
- `/catalog/my_books/` signed-in user's loans
- `/catalog/available/` librarian's available copies
- `/admin/` Django admin

## 5. Notes

- New members are added to `LibraryMember` automatically. They cannot access librarian-only actions.
- Only superusers can use the librarian pages. This is stricter and safer than merely hiding buttons in templates.
- This starter project uses SQLite locally and is suitable for coursework development. Follow your instructor's separate Canvas instructions for GitHub and PythonAnywhere deployment.
- The assignment handout and extension tutorial contain inconsistent instructor-account passwords. Follow the latest instructions provided by your instructor/Canvas; do not commit passwords to source control.
