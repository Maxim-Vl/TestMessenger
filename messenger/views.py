from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth

def index(request):
    return render(request, 'messenger/index.html')

def room(request, room_name):
    return render(request, 'messenger/room.html', {
        'room_name': room_name,
        'user': request.user.username
    })
