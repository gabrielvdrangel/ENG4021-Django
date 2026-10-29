from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Movie
from .forms import MovieForm
from django.contrib.auth.forms import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required
def home(request):

    response = requests.get("https://omdbapi.com/?apikey=38b4b85b&s=Batman&type=movie")
    
    results_json = response.json()
    
    movies = results_json["Search"]

    context = {
        "movies": movies,
    }

    return render(request, "index.html",context)

@login_required
def home2(request):

    movies = Movie.objects.all()

    return render(request, "home.html", {"movies": movies})

@login_required
def movie_create(request):

    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home2')
    else:
        form = MovieForm()

    context = {
        "form": form,
        "title": "Adicionar Filme",
    }

    return render(request, "movie_form.html", context)

@login_required
def movie_update(request, pk):

    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('home2')
    else:
        form = MovieForm(instance=movie)

    context = {
        "form": form,
        "title": "Atualizar Filme",
    }

    return render(request, "movie_form.html", context)

@login_required
def movie_delete(request, pk):

    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        movie.delete()
        return redirect('home2')

    return render(request, "movie_confirm_delete.html", {"movie": movie})

@login_required
def create_user (request):
    if request.method == 'POST':

        user = User.objects.create_user(
            request.POST['username'], 
            request.POST.get('email', ''),
            request.POST['password']
            )
        user.save()
        return redirect('home2')

    return render(request, 'register.html', context = {'action': 'Registrar'})

def login_user(request):

    if request.method == 'POST':
        user = authenticate (
            username = request.POST ['username'],
            password = request.POST ['password'] 
            )

        if user!= None:
            login(request, user)
        else:
            return render(request, 'login.html', context = {'error_msg': 'O usuário não existe'})

        if request.user.is_authenticated:
            return redirect('home2')
        return render(request, 'login.html', context = {'error_msg': 'O usuário não pode ser logado'})
    return render(request, 'login.html')

def logout_user (request):
    logout(request)
    return redirect ('login')