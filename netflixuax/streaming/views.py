from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Playlist, Recommendation
from .serializers import MovieSerializer, PlaylistSerializer, RecommendationSerializer
from django.http import JsonResponse, HttpResponse
from .utils import fetch_popular_movies, fetch_movie_details
from .scripts.import_movies import fetch_and_store_movies


# Vista Home para plantillas
def home(request):
    print("Requesting home")
    # fetch_and_store_movies()
    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})

# Vista Home para plantillas
def base(request):
    print("Requesting home")
    # fetch_and_store_movies()
    # movies = Movie.objects.all()
    return render(request, 'base.html')

# Vistas para la API
class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

class MovieDetailView(APIView):
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

class PlaylistView(APIView):
    def get(self, request):
        playlists = Playlist.objects.filter(user=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        playlist = Playlist.objects.create(name=data['name'], user=request.user)
        if 'movies' in data:
            for movie_id in data['movies']:
                movie = Movie.objects.get(id=movie_id)
                playlist.movies.add(movie)
        playlist.save()
        return Response(PlaylistSerializer(playlist).data, status=status.HTTP_201_CREATED)

class RecommendationView(APIView):
    def get(self, request):
        try:
            recommendation = Recommendation.objects.get(user=request.user)
            serializer = RecommendationSerializer(recommendation)
            return Response(serializer.data)
        except Recommendation.DoesNotExist:
            return Response({"message": "No recommendations found."}, status=status.HTTP_404_NOT_FOUND)



def popular_movies(request):
    """Vista para obtener películas populares."""
    try:
        data = fetch_popular_movies()
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def movie_details(request, movie_id):
    """Vista para mostrar detalles de una película usando la API de TMDb."""
    try:
        # Llamar a la función que interactúa con la API de TMDb
        movie_data = fetch_movie_details(movie_id)
        # Renderizar los datos en la plantilla
        return render(request, 'movie_detail.html', {'movie': movie_data})
    except Exception as e:
        return HttpResponse(f"Error al obtener detalles de la película: {str(e)}", status=500)