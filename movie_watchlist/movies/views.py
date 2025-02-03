from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Movie
from .serializers import MovieSerializer

@api_view(["POST"])
def add_movie(request):
    """Add a new movie."""
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Movie added successfully!", "movie": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_movies(request):
    """Get all movies."""
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(["PATCH"])
def update_status(request, movie_id):
    """Update a movie's watch status."""
    movie = get_object_or_404(Movie, id=movie_id)
    serializer = MovieSerializer(movie, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Status updated!", "movie": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def delete_movie(request, movie_id):
    """Delete a movie."""
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return Response({"message": "Movie deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
