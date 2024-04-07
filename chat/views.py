from django.shortcuts import render, redirect
from .forms import socketInfo


def index(request):
    if request.method == "POST":
        form = socketInfo(request.POST)
        if form.is_valid():
            socket_name = form.cleaned_data['socket_name']
            user_name = form.cleaned_data['user_name']
            print(socket_name, user_name)
            request.session['user_name'] = user_name
            return redirect('room', room_name=socket_name)
    else:
        form = socketInfo()
    return render(request, "index.html", {'form': form})


def room(request, room_name):
    user_name = request.session.get('user_name')
    if not user_name:
        return redirect('index')
    return render(request, "room.html", {"room_name": room_name, 'user_name': user_name})


def home(request):
    return render(request, "home.html")