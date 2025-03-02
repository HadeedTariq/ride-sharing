from django.shortcuts import render

from .utils import generate_refresh_access_token
from .forms import UserForm, LoginForm
from .models import User
from django.http import HttpResponseRedirect


def registerUser(request):
    successmessage = ""
    errormessage = ""
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            successmessage += "User registered successfully"
    else:
        form = UserForm()

    return render(
        request,
        "authentication/register-user.html",
        {"form": form, "successmessage": successmessage, "errormessage": errormessage},
    )


def loginUser(request):
    errormessage = ""
    successmessage = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            # Convert QuerySet to a list
            user = User.objects.get(email=email)
            if user and User.is_password_correct(password, user.password):
                successmessage += "Login successful"
                tokens = generate_refresh_access_token(user)
                if user.role == "driver":
                    response = HttpResponseRedirect("/ride/driver/home/")
                else:
                    response = HttpResponseRedirect("/ride/home/")
                response.set_cookie(
                    "access_token",
                    tokens["access_token"],
                    max_age=3600 * 10,
                    httponly=True,
                    secure=True,
                    samesite="Strict",
                )
                response.set_cookie(
                    "refresh_token",
                    tokens["refresh_token"],
                    max_age=3600 * 20,
                    httponly=True,
                    secure=True,
                    samesite="Strict",
                )
                return response
            else:
                errormessage += "Password is incorrect"
        except User.DoesNotExist:
            errormessage += "User doesn't exist"

    form = LoginForm()
    return render(
        request,
        "authentication/login-user.html",
        {
            "form": form,
            "errormessage": errormessage,
            "successmessage": successmessage,
        },
    )
