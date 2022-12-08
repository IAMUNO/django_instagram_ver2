from .models import Profile
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'EMAIL ALREADY TAKEN')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'USERNAME ALREADY TAKEN')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in and redirect to settings page

                # create profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')

        else:
            messages.info(request, 'PASSWORD NOT MATCHING')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'CREDENTIAL INVALID')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


def logout(request):
    auth.logout(request)
    return redirect('signin')
