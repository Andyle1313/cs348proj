from django.db import models

class BookReview(models.Model):
    # Fields for the book review
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author}"

    class Meta:
        # Indexes definition
        indexes = [
            models.Index(fields=['author']),  # Index on author field
            models.Index(fields=['rating']),  # Index on rating field
        ]