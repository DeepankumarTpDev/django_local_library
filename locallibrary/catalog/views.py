from typing import Any
from django.shortcuts import render
from .models import Book,BookInstance,Author,Genre
from django.views import generic
# Create your views here.


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


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        visit_count = self.request.session.get('visit_count',0)
        self.request.session['visit_count'] = visit_count + 1
        context['visit_count'] = self.request.session['visit_count']
        return context

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_details.html'