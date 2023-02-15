from cProfile import label
from dataclasses import fields
from tkinter.tix import Select
from tkinter.ttk import Style
from django import forms
from .models import Review
from .models import Movie
from .models import List
from django.forms import TextInput


class ReviewForm(forms.ModelForm):
    review_text = forms.CharField(
        label="",
        help_text="",
        widget=forms.Textarea(attrs={"style": "width:800px", "rows": 4}),
    )

    class Meta:
        model = Review
        fields = ("review_text",)


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ("name", "year", "description", "poster", "director", "genre")
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "margin-left:42px; margin-top:40px; width: 500px;",
                }
            ),
            "year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "style": "margin-left:55px; margin-top:30px; width: 500px;",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "style": "width: 500px; margin-top:30px",
                    "rows": 5,
                }
            ),
            "poster": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "width: 500px; margin-top:30px; margin-left:40px;",
                }
            ),
            "director": forms.SelectMultiple(
                choices=Movie.objects.all(),
                attrs={
                    "class": "form-control",
                    "style": "width:500px; margin-left:27px; margin-top: 30px;",
                },
            ),
            "genre": forms.SelectMultiple(
                choices=Movie.objects.all(),
                attrs={
                    "class": "form-control",
                    "style": "width:500px; margin-left:40px; margin-top: 30px;",
                },
            ),
        }


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ("name", "description", "movie")
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "margin-left:42px; margin-top:40px; width: 500px;",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "style": "width: 500px; height: 80px; margin-top:30px",
                    "rows": 5,
                }
            ),
            "movie": forms.SelectMultiple(
                choices=Movie.objects.all(),
                attrs={
                    "class": "form-control",
                    "style": "width:500px; margin-left:42px; margin-top: 30px;",
                },
            ),
        }
