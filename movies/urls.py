from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path("home/", TemplateView.as_view(template_name="home.html"), name="home"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("movie/", views.MovieListView.as_view(), name="movie_list"),
    path("addmovie/", views.MovieCreateView.as_view(), name="movie_create"),
    path("movie/<int:movie_id>/", views.MovieView.as_view(), name="movie_detail"),
    path("movie/<int:movie_id>/delete", views.MovieDeleteView.as_view(),name="movie_delete"),
    path("genre/", views.GenreListView.as_view(), name="genre_list"),
    path("genre/<int:genre_id>/", views.GenreView.as_view(), name="genre_detail"),
    path("actor/<int:actor_id>/", views.ActorView.as_view(), name="actor_detail"),
    path("director/<int:director_id>/", views.DirectorView.as_view(), name="director_detail"),
    path("movie/<int:movie_id>/review", views.ReviewListView.as_view(),name="review_list",),
    path("review/<int:review_id>/", views.ReviewView.as_view(), name="review_detail"),
    path("movie/<int:movie_id>/review/post",views.ReviewCreateView.as_view(),name="review_create"),
    path("review/<int:review_id>/delete", views.ReviewDeleteView.as_view(), name="review_delete"),
    path("review/<int:review_id>/like", views.ReviewLikeView.as_view(),name="review_like"),
    path("review/<int:review_id>/edit",views.ReviewEditView.as_view(),name="review_edit",),
    path("movie/<int:movie_id>/watchlist",views.AddToWatchlistView.as_view(),name="movie_to_watchlist"),
    path("movie/<int:movie_id>/watched",views.AddToWatchedView.as_view(),name="movie_to_watched"),
    path("movie/<int:movie_id>/like", views.LikeMovieView.as_view(), name="like_movie"),
    path("movie/<int:movie_id>/rate", views.RateMovieView.as_view(), name="rate_movie"),
    path("newlist/", views.ListCreateView.as_view(), name="list_create"),
    path("movie/<int:movie_id>/list", views.MovieToListView.as_view(), name="movie_to_list"),
    path("list/<int:list_id>", views.ListListView.as_view(), name="movie_list"),
    path("accounts/profile/<str:username>/follow", views.FollowView.as_view(),name="follow"),
    path("list/<int:list_id>/edit", views.ListEditView.as_view(), name="edit_list"),
    path("list/<int:list_id>/remove/<int:movie_id>", views.ListRemoveMovieView.as_view(), name="list_remove_movie"),
]
