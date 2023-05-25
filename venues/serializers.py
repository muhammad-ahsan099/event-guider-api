from rest_framework import serializers
# from actor.serializers import CelebrityDetailSerializer, CelebrityRoleSerializer
# from actor.serializers import CelebrityRoleSerializer
from venues.models import ImageGallery, Venue, Rating, Review, VideoGallery
# from actor.models import CelebrityDetail


class ImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageGallery
        fields = ['poster_url']


class VideoGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGallery
        fields = ['video_poster_url', 'video_url']


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        # fields = ['id', 'venue_id', 'title', 'price_per_head', 'description', 'features' ,'city',
        #           'type', 'logo_url','virtual_tour_url', 'address', 'terms_conditions','box_office', 'prime_video', 'season_title', 'season','episode', 'genre' ]
        fields = '__all__'


class VenueDetailSerializer(serializers.ModelSerializer):

    image_gallery = ImageGallerySerializer(many=True, read_only=True)
    video_gallery = VideoGallerySerializer(many=True, read_only=True)

    class Meta:
        model = Venue
        fields = '__all__'


# class GenreMoviesListSerializer(serializers.ModelSerializer):
#     genre_movies = MovieSerializer(many=True, read_only=True)

#     class Meta:
#         model = Genre
#         fields = ['id', 'title', 'imageurl', 'genre_movies']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        # fields = ['id', 'text', 'spoiler', 'likes', 'unlikes' ]

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
