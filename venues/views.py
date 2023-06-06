from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from venues.models import Venue, Rating, Review
from venues.renderers import VenueRenderer
from venues.serializers import  VenueDetailSerializer, VenueSerializer, RatingSerializer, ReviewSerializer
# from accounts.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from .paginations import HomeMoviesResultsSetPagination, MyPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from datetime import datetime, date, time, timedelta
from rest_framework.exceptions import ValidationError
from utils.utils import fetch_and_save_reviews

class VenueView(ListAPIView):
    renderer_classes = [VenueRenderer]
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        current_day = datetime.today()
        result = self.queryset.all()
        if result.exists():
            return result
        raise ValidationError(
            {
                'message': 'Result not found!',
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
            }
        )

class SearchVenues(ListAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueDetailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']



# class Top250MoviesView(ListAPIView):
#     renderer_classes = [MovieRenderer]
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     ordering = ['-imdb_rating', 'year']


# class MostPopularMoviesView(ListAPIView):
#     renderer_classes = [MovieRenderer]
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     ordering = ['-imdb_rating']

#     def get_queryset(self):
#         current_year = datetime.today().year
#         print(current_year, 'year')
#         result = self.queryset.filter(year__exact=current_year)
#         if result.exists():
#             return result
#         raise ValidationError(
#             {
#                 'message': 'Error in fetching Most popular movies',
#                 'success': False,
#                 'status': status.HTTP_404_NOT_FOUND,
#             }
#         )


# class TopPickMoviesView(ListAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     ordering = ['imdb_votes', 'metascore']
#     pagination_class = HomeMoviesResultsSetPagination

#     def get_queryset(self):
#         result = self.queryset.filter(
#             imdb_rating__gte=7, metascore__gte=80, imdb_votes__gte=500000)
#         if result.exists():
#             return result
#         raise ValidationError(
#             {
#                 'message': 'No movies in Top Pick section',
#                 'success': False,
#                 'status': status.HTTP_404_NOT_FOUND,
#             }
#         )

#     def paginate_queryset(self, queryset):
#         if self.paginator and self.request.query_params.get(self.paginator.page_query_param, None) is None:
#             return None
#         return super().paginate_queryset(queryset)



# class RecentUpcomingMoviesView(ListAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     pagination_class = HomeMoviesResultsSetPagination

#     def get_queryset(self):
#         current_day = datetime.today()
#         movies = self.queryset.filter(
#             released__gt=current_day, released__lt=current_day+timedelta(days=30))

#         if movies.exists():
#             return movies
#         raise ValidationError(
#             {
#                 'message': 'No movies in Recent',
#                 'success': False,
#                 'status': status.HTTP_404_NOT_FOUND,
#             }
#         )




class VenueDetailView(APIView):
    renderer_classes = [VenueRenderer]

    def get(self, request, pk, format=None):
        venues = Venue.objects.get(id=pk)
        serializer = VenueDetailSerializer(
            venues, context={'request': request})
        return Response(
            {
                'message': 'Successfully fetched venue detail.',
                'success': True,
                'status': status.HTTP_200_OK,
                'data': serializer.data
            },
            status=status.HTTP_200_OK)


class ReviewView(APIView):
    renderer_classes = [VenueRenderer]

    def get(self, request, format=None):

        req_url = "https://serpapi.com/search?engine=google_maps_reviews&data_id=0x3922420cf51b4e89:0x1c3e3f2c1baf3c03&api_key=e706de30a86041b5b0d85fdf57c1d109e5f583dadbab3e70979847a883c892f1"
        print('req_url: ', req_url)
        fetch_and_save_reviews(req_url)
        # venue_id = request.data['venueId']
        # reviews = Review.objects.filter(venue=venue_id)
        # serializer = ReviewSerializer(
        #     reviews, many=True, context={'request': request})
        return Response(
            {
                'message': 'Successfully fetched Reviews',
                'success': True,
                'status': status.HTTP_200_OK,
                # 'data': serializer.data
            },
            status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ReviewSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': 'Review Added Successfully',
                'success': True,
                'status': status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED)

    def patch(self, request, format=None):
        review_id = request.data['id']
        review = Review.objects.get(id=review_id)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': 'Review Updated Successfully',
                'success': True,
                'status': status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK)


class RatingView(APIView):
    renderer_classes = [VenueRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = RatingSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            {
                'message': 'Ratings to Venue Added Successfully',
                'success': True,
                'status': status.HTTP_201_CREATED,
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED)

    def put(self, request, pk, format=None):
        rating = Rating.objects.get(id=pk)
        serializer = RatingSerializer(
            rating, data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            {
                'message': 'Ratings Updated Successfully',
                'success': True,
                'status': status.HTTP_200_OK,
                'data': serializer.data
            },
            status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        rating = Rating.objects.get(id=pk)
        rating.delete()
        return Response(
            {
                'message': 'Ratings Deleted Successfully',
                'success': True,
                'status': status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK)
