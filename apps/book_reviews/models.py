from __future__ import unicode_literals
from ..login_and_registration.models import User
from django.db import models

class BookManager(models.Manager):
    def add_book(self, request):
        errors = []
        # if both author fields empty:
        if request.POST['author_name'] == "" and request.POST['new_author_name'] == "":
            errors.append('Must type Author name or select Author!')
            return (False, errors)
        # if
        elif request.POST['author_name'] == "":
            author = Author.objects.create(name=request.POST['new_author_name'])
        else:
            author = Author.objects.get(id=request.POST['author_name'])
        new_book = Book.objects.create(title=request.POST['title'], author=author)
        return (True, new_book)

class ReviewManager(models.Manager):
    def add_review(self, request, new_id):
        book = Book.objects.get(id=new_id)
        reviewer = User.objects.get(id=request.session['user']['user_id'])
        review = Review.objects.create(review_content=request.POST['review'], review_creator=reviewer, review_book=book, rating=request.POST['rating'])

    def delete_review(self, request, id):
        Review.objects.get(id=id).delete()

class Author(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    review_content = models.CharField(max_length=500)
    review_creator = models.ForeignKey(User)
    review_book = models.ForeignKey(Book, related_name='review_book')
    # positive necessary??
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()