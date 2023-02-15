from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from movies import models as movie_models

User = get_user_model()

admin.site.register(User, UserAdmin)
admin.site.register(movie_models.Movie)
admin.site.register(movie_models.Genre)
admin.site.register(movie_models.Review)
admin.site.register(movie_models.Director)
admin.site.register(movie_models.Actor)
admin.site.register(movie_models.List)
