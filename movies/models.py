from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class Actor(models.Model):
    name = models.CharField(max_length=50)
    poster = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=100)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField(null=True)
    description = models.CharField(max_length=1000, null=True)
    characters = models.ManyToManyField(Character)
    director = models.ManyToManyField(Director)
    genre = models.ManyToManyField(Genre)
    rating = models.FloatField(null=True, default=0.0)
    poster = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(
        max_length=15, unique=True, validators=[MinLengthValidator(5)]
    )
    name = models.CharField(max_length=15, null=True)
    bio = models.CharField(max_length=300, null=True)
    watched = models.ManyToManyField(Movie, related_name="watched_user")
    watchlist = models.ManyToManyField(Movie, related_name="watchlist_user")
    liked_movies = models.ManyToManyField(Movie, related_name="liked_user")
    profilepic = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=15, null=True)
    facebook = models.CharField(max_length=50, null=True)
    twitter = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.username


class UserMovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(null=True, default=None)


class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="followed_by", on_delete=models.CASCADE)


class Review(models.Model):
    review_text = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_review")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(null=True, default=None)
    likers = models.ManyToManyField(User, related_name="liked_review")
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return self.review_text


class List(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ManyToManyField(Movie)


class LikeList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
