from django.db import models
from accounts.models import User
from django.core.validators import URLValidator
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField


class ImageGallery(models.Model):
    poster_url = models.TextField(
        validators=[URLValidator()], blank=True, max_length=2000)
    # def __str__(self):
    #     return self.imageurl


class VideoGallery(models.Model):
    video_poster_url = models.TextField(
        validators=[URLValidator()], blank=True, max_length=2000)    # video = models.ImageField(upload_to='Trailers/', blank=True, storage=VideoMediaCloudinaryStorage(),
    #                           validators=[validate_video])
    video_url = models.TextField(
        validators=[URLValidator()], blank=True, max_length=2000)

    # def __str__(self):
    #     return self.videoUrl


class Venue(models.Model):
    VENUE_TYPE = (
        ('Restaurent', 'Restaurent'),
        ('Marquee', 'Marquee'),
        ('Auditorium', 'Auditorium')
    )
    venue_id = models.CharField(
        max_length=10, blank=False, unique=True, default='v3032400')
    title = models.CharField(max_length=255)
    price_per_head = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    features = ArrayField(
        models.CharField(max_length=3000), blank=True, default=list
    )
    city = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=VENUE_TYPE)
    logo_url = models.TextField(
        validators=[URLValidator()], blank=True, max_length=2000)
    virtual_tour_url = models.TextField(
        validators=[URLValidator()], blank=True, max_length=2000)
    address = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20)
    email = models.EmailField()
    image_gallery = models.ManyToManyField(ImageGallery, blank=True)
    video_gallery = models.ManyToManyField(VideoGallery, blank=True)
    capacity = models.CharField(max_length=10, blank=True)
    terms_conditions = ArrayField(
        models.CharField(max_length=1000), blank=True, default=list
    )
    total_google_reviews=models.CharField(max_length=10, null=True, blank=True)
    google_rating=models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Rating(models.Model):
    ratings = models.CharField(max_length=10)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_rating', null=True, blank=True)
    venue = models.ForeignKey(
        Venue, related_name='venue_rating', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name + ' / ' + self.venue.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review', null=True, blank=True)
    google_username = models.CharField(max_length=255, blank=True)
    google_user_thumbnail = models.TextField(validators=[URLValidator()], blank=True, max_length=2000)
    google_user_link = models.TextField(validators=[URLValidator()], blank=True, max_length=2000)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='venue_review')
    review_body = models.TextField(max_length=1000, blank=True)
    google_user_rated = models.CharField(max_length=10, null=True, blank=True)
    google_user_likes = models.PositiveIntegerField(default=0, null=True, blank=True)
    google_review_link = models.TextField(validators=[URLValidator()], blank=True, max_length=2000)
    google_review_date = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.user.name} / {self.venue.title}"
        else:
            return f"{self.google_username} / {self.venue.title}"



class ReviewLikes(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_review_like', null=True, blank=True),
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='review_like')
    likes = models.PositiveIntegerField(default=0)
    unlikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ' / ' + self.review.review_body
