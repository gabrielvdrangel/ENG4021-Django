from django.shortcuts import render
import requests
from .models import Movie
from .forms import MovieForm

def home(request):

    movies = Movie.objects.all()

    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MovieForm()


    response = requests.get("https://omdbapi.com/?apikey=38b4b85b&s=Batman&type=movie")
    
    results_json = response.json()
    
    movies = results_json["Search"]

    context = {
        "movies": movies,
        "form": form
    }

    return render(request, "index.html",context)