from django.shortcuts import render , redirect

from django.contrib.auth import logout , login , authenticate

from django.http import JsonResponse

import json

from django.forms.models import model_to_dict

from .forms import SignupForm, UpdateInfoForm

from django.contrib import messages

from .models import ActivationCode

from django.utils.timezone import now

from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required

User = get_user_model()

def user_signup(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = SignupForm(data = request.POST , files = request.FILES)

        if form.is_valid():
            user = form.save(commit=False)

            user.user_type = "client"

            password = form.cleaned_data.get("password")

            confirm_password = form.cleaned_data.get("confirm_password")

            if password != confirm_password:
                messages.warning(request, "Passwords didn't match.")
                print("Password didn't macthed")
                return render(request, "signup.html", {"form": form})

            user.set_password(password)

            user.is_active = False

            user.save(
                update_fields=[
                    "user_type",

                    "password",
                    
                    "is_active",
                ]
            )

            messages.success(request, "Account created successfully.")
            return redirect("login")

    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def activate_account(request, id, code):
    if request.user.is_authenticated:
        return redirect('login')

    _activation_code = ActivationCode.objects.filter(id = id , code = code).first()

    if not _activation_code:
        return redirect("send-activation-code")

    if now() > _activation_code.expiry_date:
        return redirect("send-activation-code")

    user = User.objects.get(email = _activation_code.user.email)

    user.is_active = True

    user.save(update_fields = ["is_active"])

    return redirect("login")


@login_required(login_url="login")
def update_info(request):

    user = request.user

    if request.method == "POST":
        form = UpdateInfoForm(
            data=request.POST,
            files=request.FILES,
            instance=user
        )

        if form.is_valid():
            form.save()
            return redirect('update-info')

        else:
            return redirect('update-info')

    else:
        form = UpdateInfoForm(instance=user)

    return render(request, "update-info.html", {
        "form": form
    })

    return render(request , "update-info.html", {"form":form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        data = json.loads(request.body)

        username = data.pop("username")

        password = data.pop("password")

        user = authenticate(request , username = username , password = password)

        if user:
            login(request , user)
            return JsonResponse({"success":True})

        else:
            return JsonResponse({"success":False})

    return render(request , "login.html")

    

def user_logout(request):

    if not request.user.is_authenticated:

        return redirect("index")

    logout(request)

    return redirect("index")