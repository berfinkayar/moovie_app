from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.db.models import Q
from .forms import SignUpForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from movies.models import Review, UserFollowing, List
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "registration/signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return render(request, "registration/signup.html", {"form": form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, username):
        requestmaker = request.user
        user = get_object_or_404(User, username=username)

        is_following = UserFollowing.objects.filter(
            Q(user=user) & Q(following_user=requestmaker)
        )
        followers = UserFollowing.objects.filter(user=user)
        following = UserFollowing.objects.filter(following_user=user)
        lists = List.objects.filter(user=user)

        review_list = Review.objects.filter(user=user).order_by("-date")
        review_dict = {}

        for review in review_list:
            if review.likers.filter(pk=requestmaker.id):
                review_dict[review] = 1
            else:
                review_dict[review] = 0

        return render(
            request,
            "accounts/profile.html",
            {
                "requested_user": user,
                "is_following": is_following,
                "followers": followers,
                "following": following,
                "lists": lists,
                "review_dict": review_dict,
            },
        )


class EditProfileView(View):
    def get(self, request):
        return render(request, "accounts/editprofile.html", {})

    def post(self, request):
        form = request.POST
        user = request.user
        user.username = form["username"]
        user.name = form["name"]
        user.email = form["email"]
        user.bio = form["bio"]
        user.location = form["location"]
        user.profilepic = form["profile"]
        user.facebook = form["facebook"]
        user.twitter = form["twitter"]
        user.save()
        return redirect(reverse("profile", kwargs={"username": user.username}))


class ChangePasswordView(View):
    def post(self, request):
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        if old_password and new_password and confirm_password:
            user = User.objects.get(pk=request.user.id)
            if not user.check_password(old_password):
                messages.warning(request, "Old password is not correct!")
            elif len(new_password) < 8:
                messages.warning(
                    request, "New password should contain 8 characters minimum!"
                )
            else:
                if new_password != confirm_password:
                    messages.warning(
                        request, "New password not match the confirm password!"
                    )

                else:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "Password has been changed successfully.")
                    return redirect(
                        reverse("profile", kwargs={"username": request.user.username})
                    )
        else:
            messages.warning(request, "All fields are required!")
        return redirect("edit_profile")
