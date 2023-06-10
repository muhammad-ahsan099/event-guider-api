import requests
from django.core.exceptions import ValidationError
from venues.models import Review, Venue


def fetch_and_save_reviews(url):
    # Make the HTTP request to fetch reviews
    response = requests.get(url)
    reviews_data = response.json().get("reviews", [])

    # Process each review and save them into the database
    current_venue = Venue.objects.get(id=24)
    for review_data in reviews_data:
        # Extract relevant fields from the review_data
        link = review_data.get("link")
        rating = review_data.get("rating")
        snippet = review_data.get("snippet")
        likes = review_data.get("likes")
        review_date = review_data.get("date")

        user_data = review_data.get("user", {})
        user_name = user_data.get("name")
        user_link = user_data.get("link")
        user_thumbnail = user_data.get("thumbnail")

        # Create a new Review object and save it

        print("Review Data:")
        print("google_username", user_name)
        print("user_thumbnail:", user_thumbnail)
        print("Snippet:", snippet)
        print("Likes:", likes)
        print("User rating:", rating)
        print("User Link:", user_link)
        print("User Thumbnail:", user_thumbnail)
        print("google_review_link:", link)
        print("Review snippet:", snippet)
        print("Review review_date:", review_date)

        review = Review.objects.create(
            google_username=user_name,
            google_user_thumbnail=user_thumbnail,
            venue=current_venue,
            review_body=snippet,
            google_user_rated=rating,
            google_user_likes=likes,
            google_review_link=link,
            google_review_date=review_date,
            google_user_link=user_link
        )


        review.save()
