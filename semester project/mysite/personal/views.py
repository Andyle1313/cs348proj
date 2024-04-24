from django.shortcuts import render, redirect
from .models import BookReview
from .forms import BookReviewForm
from django.urls import reverse_lazy
from django.db.models import Avg
from django.db import connection

def book_statistics(request):
    avg_rating = None
    num_reviews = None
    book_title = None  # Initialize book_title variable

    if request.method == 'POST':
        book_title = request.POST.get('book_title')

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT AVG(rating) FROM personal_bookreview WHERE title = %s", [book_title])
                avg_rating = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM personal_bookreview WHERE title = %s", [book_title])
                num_reviews = cursor.fetchone()[0]
        except Exception as e:
            # Log the exception or handle it in an appropriate way
            print("An error occurred:", e)

    return render(request, 'book_statistics.html', {'avg_rating': avg_rating, 'num_reviews': num_reviews, 'book_title': book_title})



def author_statistics(request):
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        # Retrieve books and calculate average rating for the given author
        books = BookReview.objects.filter(author=author_name)
        avg_rating = books.aggregate(avg_rating=Avg('rating'))['avg_rating']

        return render(request, 'statistics.html', {'author_statistics': {'avg_rating': avg_rating, 'books': books}, 'author_name': author_name})

    return render(request, 'statistics.html')

def statistics(request):
    # Calculate average ratings for authors
    authors_avg_ratings = BookReview.objects.values('author').annotate(avg_rating=Avg('rating'))

    return render(request, 'statistics.html', {'authors_avg_ratings': authors_avg_ratings})

def review_list(request):
    # Retrieve all reviews from the database
    reviews = BookReview.objects.all()
    return render(request, 'reviews.html', {'reviews': reviews})

def add_review(request):
    if request.method == 'POST':
        # Process the form submission
        form = BookReviewForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            return redirect('reviews')  # Redirect to the reviews page after successful submission
    else:
        # Display the form for adding a new review
        form = BookReviewForm()

    return render(request, 'reviews.html', {'form': form})


# Create your views here.

def home_screen_view(request):
    return render(request, "base.html", {})

def reviews_screen_view(request):
    return render(request, "reviews.html", {})

def base_screen_view(request):
    return render(request, "base.html", {})