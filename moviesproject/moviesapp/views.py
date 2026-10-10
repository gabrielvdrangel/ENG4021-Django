from django.shortcuts import render
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


    context = {
        "movies": movies,
        "form": form
    }

    return render(request, "index.html",context)