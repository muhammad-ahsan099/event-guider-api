from django.contrib import admin
from venues.models import ImageGallery, Venue, Rating, Review, ReviewLikes, VideoGallery


# admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(ReviewLikes)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'venue_id', 'title', 'price_per_head', 'description', 'features' ,'city',
                  'type', 'logo_url','virtual_tour_url' )
    

@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'poster_url')


@admin.register(VideoGallery)
class VideoGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_poster_url')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'ratings', 'user', 'venue')
