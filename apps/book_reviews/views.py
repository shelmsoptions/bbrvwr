from django.shortcuts import render, redirect
from ..login_and_registration.models import User
from models import Book, Author, Review
from django.contrib import messages

def user_in_session(request):
    if 'user' in request.session:
        # print 'method - user in sessions True!!'
        return True
    else:
        # print 'method - user in sessions False!!'
        return False

def index(request):
    if user_in_session(request):
        context = {
            'recent_reviews': Review.objects.order_by('-created_at')[:4],
            'all_books': Book.objects.all(),
            # 'all_reviews': Review.objects.values('review_book').distinct(),
        }
        return render(request, 'book_reviews/index.html', context)
    return redirect('login:index')

def add_form(request):
    if 'user' in request.session:
        context = {
            'authors': Author.objects.all()
        }
        # print context['authors']
        return render(request, 'book_reviews/add.html', context)
    return redirect('login:index')

def add_book_and_review(request):
    # print 'in add_book_and_review method'
    # print type(request)
    # print request
    if user_in_session(request):
        result = Book.objects.add_book(request)
        if result[0] == False:
            display_errors(request, result[1])
            print display_errors
            return redirect('book:editor')
        # review created - add_review method 'assigns' it to
        Review.objects.add_review(request, result[1].id)
    return redirect('login:index')

def add_review(request, id):
    Review.objects.add_review(request, id)
    print request
    return redirect('book:show_book', id)


def delete_review(request, review_id, book_id):
    # crap - need unique id's for book_ and review_ if I wanna stay on current book review !!!
    # print id
    # print book_id
    if user_in_session(request):
        Review.objects.delete_review(request, review_id)
    return redirect('book:show_book', book_id)

def display_errors(request, display_errors_list):
    for error in display_errors_list:
        #  VV    https://docs.djangoproject.com/en/1.10/ref/contrib/messages/    VV
        messages.add_message(request, messages.INFO, error)

def show_book(request, id):
    if user_in_session(request):
        # print Book.objects.get(id=id).title
        context = {
            'book': Book.objects.get(id=id),
            'reviews': Review.objects.filter(review_book=id)
        }
        return render(request, 'book_reviews/book.html', context)
    return redirect('login:index')

def show_user(request, id):
    if user_in_session(request):
        # print User.objects.get(id=id).first_name
        context = {
            'user': User.objects.get(id=id),
            # VV WHOA!!  https://docs.djangoproject.com/en/1.10/topics/db/queries/  VV  Lookups that span relationships - ALSO related_name (book_review)!!!
            'books_reviewed': Book.objects.filter(review_book__review_creator__id=id),
            'review_count': Book.objects.filter(review_book__review_creator__id=id).count(),
        }
        return render(request, 'book_reviews/user.html', context)
    return redirect('login:index')