from django.contrib import admin
from django.http import HttpResponseRedirect


from .models import Author, Genre, Book, BookInstance, Language, Parsing

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


class BookInLine(admin.TabularInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', )
    fields = ['name']
    inlines = [BookInLine]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre')
    list_filter = ('author', 'genre')
    inlines = [BooksInstanceInline]
    change_list_template = "admin/model_change_list.html"


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )






