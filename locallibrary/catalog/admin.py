from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

class BooksInline(admin.TabularInline):
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
     list_display = ('title', 'author', 'display_genre')
     inlines = [BooksInstanceInline]



@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book','status','due_back','id')
    fieldsets = (
        (None,{'fields':('book', 'imprint', 'id')}),
        ('Availability',{'fields':('status', 'due_back')})
    )
    

#admin.site.register(Book)
#admin.site.register(Author, AuthorAdmin)  We directly add decorater to register it in admin
admin.site.register(Genre)
#admin.site.register(BookInstance)
admin.site.register(Language)
