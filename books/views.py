from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from django.views.generic import View, DetailView
from django.db.models import Count
from .forms import ReviewForm, BookForm
from django.core.urlresolvers import reverse


def list_books(request):
    """
    List the books that have reviews
    """
    books = Book.objects.exclude(
        date_reviewed__isnull=True).prefetch_related(
        'authors')
    return render(
        request, "list.html",
        locals())


class AuthorList(View):
    def get(self, request):

        authors = Author.objects.annotate(
            published_books=Count('books')).filter(
            published_books__gt=0)

        return render(request,
                      'authors.html',
                      locals())


class AuthorDetail(DetailView):
    model = Author
    template_name = 'author.html'


class BookDetail(DetailView):
    model = Book
    template_name = 'book.html'


def review_books(request):
    """ List all the books that we want to review"""
    books = Book.objects.filter(
        date_reviewed__isnull=True).prefetch_related('authors')

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid()
        form.save()
    else:
        form = BookForm()
        return redirect('review-books')
    return render(
        request, 'list-to-review.html', locals())


def review_book(request, pk):
    """ Review an Individual book """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            book.is_favourite = form.cleaned_data['is_favourite']
            book.review = forms.cleaned_data['review']
            book.reviewed_by = request.user
            book.save()

            return redirect('review-books')
    else:
        form = ReviewForm()
    return render(request, "review-book.html",
                  locals())
