from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Movie

# movie/views.py
from google import genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

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

# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages


def login_choice(request):
    # Page with buttons: User Login / Admin Login
    return render(request, "movies/login_choice.html")


def ensure_demo_users():
    demo_users = [
        {"username": "demo", "password": "DemoPass123"},
        {"username": "alice", "password": "AlicePass"},
        {"username": "bob", "password": "1234"},
    ]

    for user_data in demo_users:
        user, created = User.objects.get_or_create(username=user_data["username"])
        # Only set password if user was just created or password is unusable
        if created or not user.has_usable_password():
            user.set_password(user_data["password"])
            user.save()


def user_login(request):
    ensure_demo_users()  # make sure demo users exist

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("user_home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "movies/user_login.html")


@login_required(login_url="user_login")
def user_home(request):
    # Your current home.html page with AI recommendations
    return render(request, "movies/user_home.html")
