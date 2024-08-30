from typing import Any
from django.shortcuts import render
from .models import Book,BookInstance,Author,Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()


    #Keeptracking of session info
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits


    num_BooksContains_Murder = Book.objects.filter(title__icontains = 'murder').count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres' : num_genres,
        'num_BooksContains_Murder' : num_BooksContains_Murder,
        'num_visits' : num_visits
    }
    return render(request, 'index.html', context = context)


class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    paginate_by = 2

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        visit_count = self.request.session.get('visit_count',0)
        self.request.session['visit_count'] = visit_count + 1
        context['visit_count'] = self.request.session['visit_count']
        return context

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin,generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(LoginRequiredMixin,generic.DetailView):
    model = Author
    template_name = 'catalog/author_details.html'

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    
from django.contrib.auth.mixins import PermissionRequiredMixin

class BorrowedBooksByUserLibrarianListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/loaned_books_list_librarian.html'
    context_object_name = 'loaned_books'
    paginate_by = 10
    permission_required = ('catalog.can_mark_returned', 'catalog.change_book')  # change_book => Builtin permission
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact = 'o').order_by('due_back')
    