from django.db import models
from datetime import date

from bs4 import BeautifulSoup
from urllib.request import urlopen
# Чтобы парсить

from django.urls import reverse
# Чтобы сгенерировать URL по паттернам

import uuid
# Для уникальных id

from django.contrib.auth.models import User


class Genre(models.Model):
    """ Модель, представляющая жанры книг"""
    name = models.CharField(max_length=200, help_text="Введите жанр книги")

    def __str__(self):
        return self.name


class Book(models.Model):
    """ Модель, представляющая книги """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # ForeignKey использую, потому что книга может иметь только одного автора, но автор много книг
    summary = models.TextField(max_length=1000, help_text='Введите краткое описание книги')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 символова <a href="https://www.isbn-international.org/content/what-isbn">ISBN номера</a> книги')
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('Language', max_length=20, on_delete=models.SET_NULL, null=True)
    rating = models.ForeignKey('Rating', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ Возвращает URL для доступа к странице книги"""
        return reverse('book-detail', args=[str(self.id)])

    # def display_genre(self):
    #     return ', '.join([genre.name for genre in self.genre.all()[:3]])
    #
    # display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """ Модель представляет спецификацию копий книг """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальное id для конкретной книги")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200, default='Default')
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'Выдана'),
        ('a', 'Доступна'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Доступность книги')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)

    def display_book(self):
        return ', '.join(self.book)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    """ Модель представляет автора """
    name = models.CharField(max_length=100)

    # last_name = models.CharField(max_length=100)
    # date_of_birth = models.DateField(null=True, blank=True)
    # date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """ Возвращает url для доступа к странице автора"""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{}'.format(self.name)


class Language(models.Model):
    """ Модель представляющая язык """
    name = models.CharField(max_length=200, help_text="Введите язык книги")

    def __str__(self):
        return self.name


class Rating(models.Model):
    """ Модель для оценок """
    rate = models.BigIntegerField(help_text='Поставьте оценку')


""" Далее -- парсинг данных с книжного сайта"""


class Parsing:

    def __init__(self):
        self.page = 1
        self.html_doc = urlopen(f'https://www.litmir.me/bs?rs=5%7C1%7C0&o=100&p={str(self.page)}').read()
        self.soup = BeautifulSoup(self.html_doc)
        self.cards = self.soup.find_all('table', style='max-height:750px;')

    """ Парсинг данных (вычленение) """

    def get_author(self, card):
        return card.find('span', itemprop='author').find_all('a')[0].get_text()

    def get_genre(self, card):
        return card.find('span', itemprop='genre').find_all('a')[0].get_text()

    def get_book_title(self, card):
        return card.select('span', itemprop='name')[0].get_text()

    def get_book_summary(self, card):
        try:
            return card.find('div', class_='item_description').find('p').get_text()
        except AttributeError:
            return "Empty"


    """ Загрузка данных в базу """

    def load_authors(self):
        for card in self.cards:
            Author.objects.get_or_create(name=self.get_author(card))

    def load_genres(self):
        for card in self.cards:
            Genre.objects.get_or_create(name=self.get_genre(card))

    def load_books(self):
        for card in self.cards:
            Book.objects.get_or_create(title=self.get_book_title(card),
                                       author=Author.objects.get(name=self.get_author(card)),
                                       summary=self.get_book_summary(card),
                                       isbn='2883723872178',
                                       genre=Genre.objects.get(name=self.get_genre(card)),
                                       language=Language.objects.get(name='Русский'))

    def parse_one_page(self):
        self.load_authors()
        self.load_genres()
        self.load_books()

    def parse_all_pages(self):
        for i in range(5996):
            self.page = i
            self.html_doc = urlopen(f'https://www.litmir.me/bs?rs=5%7C1%7C0&o=100&p={str(self.page)}').read()
            self.soup = BeautifulSoup(self.html_doc)
            self.cards = self.soup.find_all('table', style='max-height:750px;')
            self.load_authors()
            self.load_genres()
            self.load_books()


