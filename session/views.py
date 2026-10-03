from django.shortcuts import render , redirect

from django.contrib.auth import logout , login , authenticate

from django.http import JsonResponse

import json, uuid

from django.forms.models import model_to_dict

from .forms import SignupForm, UpdateInfoForm, ChangePasswordForm

from django.contrib import messages

from .models import ActivationCode

from django.utils.timezone import now

from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required

import random

from threading import Thread

from core.services.send_mail import EmailService

from django.contrib.auth import update_session_auth_hash

from datetime import timedelta , datetime

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

@login_required(login_url="login")
def change_password(request):
    form = ChangePasswordForm()
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST)

        if form.is_valid():
            old_password = form.cleaned_data.get("old_password")
            new_password = form.cleaned_data.get("new_password")
            confirm_password = form.cleaned_data.get("confirm_password")

            if not request.user.check_password(old_password):
                messages.warning(request, "Wrong old password")
                return render(request, "change-password.html", {"form": form})

            if request.user.check_password(new_password):
                messages.warning(request, "New password cannot be the same as your old password.")
                return render(request, "change-password.html", {"form": form})

            if new_password != confirm_password:
                messages.info(request, "OOPS! Password didn't match")
                return render(request, "change-password.html", {"form": form})

            request.session["code"] = str(random.randint(1000, 9999))
            request.session["password_change_key"] = f"{request.user.id}-{now()}-{uuid.uuid4()}"
            request.session["password"] = confirm_password

            email_thread = Thread(
                target=EmailService.send_mail,
                args=(
                    [request.user.email],
                    "Password change code",
                    f"Hey, {request.user.get_full_name()}.\nWe noticed someone trying to change your account password. This is the code {request.session.get('code')} to confirm this action.\nIf this wasn't you, please change your password immediately and don't share this code with anyone.",
                ),
            )
            email_thread.start()

            return redirect("verify-change-password-code")

    return render(request, "change-password.html", {"form": form})


@login_required(login_url="login")
def verify_change_password_code(request):
    password_change_key = request.session.get("password_change_key", None)

    if not password_change_key:
        return redirect("change-password")

    if request.method == "POST":
        attempts = request.session.get("attempts", 1)
        session_code = request.session.get("code", None)
        user_code = request.POST.get("code", None)  
        password = request.session.get("password")

        if attempts > 3:
            request.session.pop("code", None)
            request.session.pop("password", None)
            request.session.pop("password_change_key", None)
            request.session.pop("attempts", None)
            return redirect("change-password")

        if not session_code:
            messages.warning(request, "OOPS! Code not found or expired.")
            return redirect("change-password")
        
        if int(session_code) == int(user_code):
            user = request.user
            user.set_password(password)
            user.save()
            
            update_session_auth_hash(request, user)

            request.session.pop("code", None)
            request.session.pop("password", None)
            request.session.pop("password_change_key", None)
            request.session.pop("attempts", None)

            return redirect("index") 
        else:
            attempts += 1
            request.session["attempts"] = attempts 
            messages.warning(request, f"Wrong verification code! Attempt {attempts-1}/3")

    return render(request, "verify-code.html")



def resend_code(request):
    password_change_key = request.session.get("password_change_key", None)

    if not password_change_key:
        return redirect("change-password")

    prev_code = request.session.get("code", None)

    del prev_code  # Delete the previous code to ensure a new one is generated

    del password_change_key # Delete the previous password change key to ensure a new one is generated

    request.session["code"] = str(random.randint(1000, 9999))
    request.session["password_change_key"] = f"{request.user.id}-{now().strftime('%Y-%m-%d %H:%M:%S')}-{uuid.uuid4()}"
    email_thread = Thread(
        target=EmailService.send_mail,
        args=(
            [request.user.email],
            "Password change code",
            f"Hey, {request.user.get_full_name()}.\nWe noticed someone trying to change your account password. This is the code {request.session.get('code')} to confirm this action",
        ),
    )
    email_thread.start()
    messages.success(request, "New code sent!")
    return redirect("verify-change-password-code")
