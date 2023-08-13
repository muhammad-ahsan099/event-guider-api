from django.urls import path
from venues.views import VenueView, VenueDetailView, RatingView, ReviewView, MostPopularVenuesView, RecommendedVenuesView, SearchVenues, ViewedVenues
urlpatterns = [
    path('home-venues/', VenueView.as_view(), name='venue'),
    path('venue/<int:pk>', VenueDetailView.as_view(), name='venue-detail'),
    path('most-popular-venues/', MostPopularVenuesView.as_view(), name='most-popular-venue'),
    path('recommended-venues/', RecommendedVenuesView.as_view(), name='recommended-venues'),
    path('viewed_venues/', ViewedVenues.as_view(), name='viewed_venues'),
    path('search-venues/', SearchVenues.as_view(), name='venues-search'),
    path('review/', ReviewView.as_view(), name='review'),
    path('rating/', RatingView.as_view(), name='rating'),
    path('rating/<int:pk>/', RatingView.as_view(), name='rating-update'),

]
