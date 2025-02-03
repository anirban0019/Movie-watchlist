from django.urls import path
from .views import add_movie, get_movies, update_status, delete_movie

urlpatterns = [
    path("add/", add_movie, name="add_movie"),
    path("list/", get_movies, name="get_movies"),
    path("update/<int:movie_id>/", update_status, name="update_status"),
    path("delete/<int:movie_id>/", delete_movie, name="delete_movie"),
]
