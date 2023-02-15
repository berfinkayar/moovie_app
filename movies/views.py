import requests
from platform import release
from django.views import View
from django.db.models import Sum, Count, Q
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MovieForm, ListForm, ReviewForm
from .models import Character, Movie, UserMovieRating, User, List, UserFollowing, Genre, Actor, Review, Director


class MovieView(View):
    def get(self, request, movie_id):
        user = request.user
        reviewForm = ReviewForm()
        movie = Movie.objects.get(pk=movie_id)

        review_list = Review.objects.filter(movie=movie).order_by("-date")[:3]
        review_dict = {}
        for review in review_list:
            if review.likers.filter(pk=request.user.id):
                review_dict[review] = 1
            else:
                review_dict[review] = 0

        character_list = Character.objects.filter(movie=movie).order_by("order")
        watched = (
            user.watched.filter(pk=movie_id) 
            if user.is_authenticated 
            else []
        )
        in_watchlist = (
            user.watchlist.filter(pk=movie_id) 
            if user.is_authenticated 
            else []
        )
        liked = (
            request.user.liked_movies.filter(pk=movie_id)
            if user.is_authenticated
            else []
        )
        lists = (
            List.objects.filter(user=user) 
            if user.is_authenticated 
            else []
        )
        friend_list = (
            user.followed_by.filter(following_user=user)
            if user.is_authenticated
            else []
        )
        
        friend_activity = [friend.user for friend in friend_list if friend.user.watched.filter(pk=movie_id)]

        is_rated = (
            UserMovieRating.objects.filter(Q(user=user) & Q(movie=movie))
            if user.is_authenticated
            else False
        )
        user_rating = is_rated[0].rating if is_rated else 0

        return render(
            request,
            "movies/movie_detail.html",
            {
                "movie": movie,
                "review_dict": review_dict,
                "review_form": reviewForm,
                "character_list": character_list,
                "watched": watched,
                "in_watchlist": in_watchlist,
                "liked": liked,
                "lists": lists,
                "user_rating": user_rating,
                "friends": friend_activity,
            },
        )

class MovieListView(ListView):
    model = Movie
    template_name = "movies/movie_index.html"
    context_object_name = "movie_list"
    paginate_by = 25
    queryset = Movie.objects.all().order_by("-year")


class MovieCreateView(View):
    def get(self, request):
        form = MovieForm()
        return render(request, "movies/add_movie.html", {"form": form,})

    def post(self, request):
        form = MovieForm(request.POST)
        if form.is_valid() and request.user.is_superuser:
            movie = form.save()
            return redirect(reverse("movie_detail", kwargs={"movie_id": movie.id}))
        else:
            return render(request, "movies/add_movie.html", {"form": form})


class MovieDeleteView(View):
    def get(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)

        if request.user.is_superuser:
            movie.delete()

        return redirect(reverse("movie_list"))


class SearchView(View):
    def get(self, request):
        query_dict = request.GET
        query = query_dict['q']
        if query is not None:
            movie_list = Movie.objects.filter(
                name__icontains=query
            )
        context = {"movie_list": movie_list, "search_key": query}
        return render(request, "movies/movie_index.html", context)


class GenreView(View):
    def get(self, request, genre_id):
        genre = Genre.objects.get(pk=genre_id)
        movie_list = Movie.objects.filter(genre=genre).order_by("-year")
        context = {"movie_list": movie_list, "genre_name": genre.name}
        return render(request, "movies/movie_index.html", context)


class GenreListView(View):
    def get(self, request):
        genre_list = Genre.objects.all().order_by("name")
        genre_dict = {}
        for genre in genre_list:
            movies = Movie.objects.filter(genre=genre)
            genre_dict[genre] = movies
        return render(request, "movies/genre_index.html", {"genre_dict": genre_dict,})


class ActorView(View):
    def get(self, request, actor_id):
        actor = get_object_or_404(Actor, pk=actor_id)
        characters = Character.objects.filter(actor=actor)
        movies = []
        for character in characters:
            movie_exists = Movie.objects.filter(characters=character)
            if movie_exists:
                movies.append(movie_exists[0])
        return render(
            request, "movies/actor_detail.html", {"actor": actor, "movie_list": movies}
        )


class DirectorView(View):
    def get(self, request, director_id):
        director = get_object_or_404(Director, pk=director_id)
        movies = Movie.objects.filter(director=director)
        return render(
            request,
            "movies/director_detail.html",
            {"director": director, "movie_list": movies},
        )


class ReviewView(View):
    def get(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        liked = review.likers.filter(pk=request.user.id)
        return render(
            request, "movies/review_detail.html", {"review": review, "liked": liked}
        )


class ReviewListView(View):
    def get(self, request, movie_id):
        review_list = Review.objects.filter(movie=movie_id).order_by("-date")
        review_dict = {}
        for review in review_list:
            if review.likers.filter(pk=request.user.id):
                review_dict[review] = 1
            else:
                review_dict[review] = 0

        return render(request, "movies/review_index.html", {"review_dict": review_dict})


class ReviewCreateView(LoginRequiredMixin, View):
    def get(self, request, movie_id):
        return redirect(reverse("movie_detail", kwargs={"movie_id": movie_id}))

    def post(self, request, movie_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_text = form.cleaned_data["review_text"]
            movie = Movie.objects.get(pk=movie_id)
            review = Review(review_text=review_text, user=request.user, movie=movie)
            review.save()
            return redirect(reverse("movie_detail", kwargs={"movie_id": movie_id}))

        else:
            return render(request, "movies/movie_detail.html", {"form": form})


class ReviewDeleteView(View):
    def get(self, request, review_id):
        review = Review.objects.get(pk=review_id)
        if review.user == request.user or request.user.is_superuser:
            review.delete()
        return redirect(reverse("movie_detail", kwargs={"movie_id": review.movie.id}))


class ReviewEditView(View):
    def post(self, request, review_id):
        review = Review.objects.get(pk=review_id)
        form = request.POST
        review.review_text = form["review_text"]
        review.save()
        return redirect(reverse("movie_detail", kwargs={"movie_id": review.movie.id}))


class ReviewLikeView(View):
    def get(self, request, review_id):
        user = request.user
        review = Review.objects.get(pk=review_id)
        is_liked = review.likers.filter(pk=user.id)

        if not is_liked:
            review.likers.add(user)
            review.like_count += 1

        else:
            review.likers.remove(user)
            review.like_count -= 1

        review.save()
        return redirect(reverse("movie_detail", kwargs={"movie_id": review.movie.id}))


class FollowView(View):
    def get(self, request, username):
        followed = User.objects.get(username=username)
        followed_by = request.user
        is_following = UserFollowing.objects.filter(
            Q(user=followed) & Q(following_user=followed_by)
        )

        if not is_following:
            follow_relation = UserFollowing(user=followed, following_user=followed_by)
            follow_relation.save()
        else:
            is_following.delete()
        return redirect(reverse("profile", kwargs={"username": username}))


class AddToWatchlistView(View):
    def get(self, request, movie_id):
        user = request.user
        movie = Movie.objects.get(pk=movie_id)
        in_watchlist = user.watchlist.filter(pk=movie_id)

        if not in_watchlist:
            user.watchlist.add(movie)
        else:
            user.watchlist.remove(movie)
        return redirect(reverse("movie_detail", kwargs={"movie_id": movie_id}))


class AddToWatchedView(View):
    def get(self, request, movie_id):
        user = request.user
        movie = Movie.objects.get(pk=movie_id)
        is_watched = user.watched.filter(pk=movie_id)

        if not is_watched:
            user.watched.add(movie)
        else:
            user.watched.remove(movie)
        return redirect(reverse("movie_detail", kwargs={"movie_id": movie_id}))


class LikeMovieView(View):
    def get(self, request, movie_id):
        user = request.user
        movie = Movie.objects.get(pk=movie_id)
        liked = user.liked_movies.filter(pk=movie_id)

        if not liked:
            user.liked_movies.add(movie)
        else:
            user.liked_movies.remove(movie)
        return redirect(reverse("movie_detail", kwargs={"movie_id": movie_id}))


class MovieToListView(LoginRequiredMixin, View):
    def post(self, request, movie_id):
        list_id = request.POST["list"]
        list = List.objects.get(pk=list_id)
        movie = Movie.objects.get(pk=movie_id)
        in_list = list.movie.filter(pk=movie_id)
        if not in_list:
            list.movie.add(movie)
        return redirect(reverse("movie_detail", kwargs={"movie_id": movie_id}))


class ListListView(View):
    def get(self, request, list_id):
        list = List.objects.get(pk=list_id)
        movies = list.movie.all()
        context = {
            "movie_list": movies,
            "list": list,
        }
        return render(request, "movies/movie_index.html", context)


class ListCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ListForm()
        return render(request, "movies/new_list.html", {"form": form,})

    def post(self, request):
        form = ListForm(request.POST)
        if form.is_valid():
            movie_list = List(
                name=form.cleaned_data["name"],
                user=request.user,
                description=form.cleaned_data["description"],
            )
            movie_list.save()
            movie_list.movie.set(form.cleaned_data["movie"])
            context = {
                "movie_list": movie_list.movie.all(),
                "list": movie_list,
            }
            return render(request, "movies/movie_index.html", context)

        else:
            return render(request, "movies/new_list.html", {"form": form})


class RateMovieView(LoginRequiredMixin, View):
    def get(self, request, movie_id):
        return redirect(reverse("movie_detail", kwargs={"movie_id": movie_id}))
        
    def post(self, request, movie_id):
        rating = float(request.POST["star"]) / 2
        movie = Movie.objects.get(pk=movie_id)
        is_rated = UserMovieRating.objects.filter(Q(user=request.user) & Q(movie=movie))

        if is_rated:
            is_rated[0].rating = rating
            is_rated[0].save()

        else:
            rate = UserMovieRating(user=request.user, movie=movie, rating=rating)
            rate.save()

        total_rating = UserMovieRating.objects.filter(movie=movie).aggregate(
            Sum("rating")
        )["rating__sum"]
        rater_count = UserMovieRating.objects.filter(movie=movie).count()
        movie.rating = total_rating / rater_count
        movie.save()
        return redirect(reverse("movie_detail", kwargs={"movie_id": movie_id}))

class ListEditView(View):
    def get(self, request, list_id):
        list = List.objects.get(pk=list_id)
        movies = list.movie.all()
        context = {
            "movies": movies,
            "list":list,
        }
        return render(request, "movies/list_edit.html", context)

class ListRemoveMovieView(View):
    def get(self, request, list_id, movie_id):
        list = List.objects.get(pk=list_id)
        movie = Movie.objects.get(pk=movie_id)
        list.movie.remove(movie)
        return redirect(reverse("edit_list", kwargs={"list_id": list_id}))
