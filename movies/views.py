from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Movie

# movie/views.py
from google import genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Hardcode your API key (for hackathon/demo only)
client = genai.Client(api_key="AIzaSyDX2RElhuO3SgSHLlnMn2S2R2M4LBI8rtQ")


@csrf_exempt
def ai_recommendations(request):
    try:
        data = json.loads(request.body)
        user_movies = data.get("movies", "")

        prompt = f"""You are a movie recommendation assistant.
User likes: {user_movies}.
Recommend 3 similar movies with reasons as a simple paragraph"""
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )

        return JsonResponse({"recommendations": response.text})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Create your views here.
def index(request):
    movies = Movie.objects.all()
    # Movie.objects.filter(release_year=1990)
    # Movie.objects.get(id=1)
    # output = ", ".join([m.title for m in movies])
    return render(request, "movies/index.html", {"movies": movies})


def detail(request, movie_id):
    # should supply the model class and data id to query
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, "movies/details.html", {"movie": movie})


# or


# try:
#     movie = Movie.objects.get(id=movie_id)
#     return render(request, 'movies/details.html', {'movie':movie})
# except Movie.DoesNotExist :
#     raise Http404
