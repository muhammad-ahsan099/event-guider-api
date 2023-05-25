from email.policy import default
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.response import Response
from rest_framework import status


class HomeMoviesResultsSetPagination(PageNumberPagination):
    page_size = 18
    page_size_query_param = 'page_size'
    max_page_size = 18



class MyPagination(PageNumberPagination):
    page_size = 15
    max_page_size = 15
