from django.db import models

class ReviewRating(models.Model):
    # user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=30, blank=True)
    name = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    review = models.TextField(max_length=2000, blank=True, null=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject
    
    def guestname(self):
        return self.email.split('@')[0].lower()
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def averageRating(self):
        totalRating = ReviewRating.object.values('rating')
        avg = sum(totalRating) / len(totalRating)
        return avg
