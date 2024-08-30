from django.shortcuts import render
from .models import Book,BookInstance,Author,Genre
from django.views import generic
# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()

    num_BooksContains_Murder = Book.objects.filter(title__icontains = 'murder').count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres' : num_genres,
        'num_BooksContains_Murder' : num_BooksContains_Murder
    }
    return render(request, 'index.html', context = context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book