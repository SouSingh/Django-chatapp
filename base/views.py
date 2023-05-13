from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm,TopicForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm



def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_message': room_message}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    roommessages = room.message_set.all() 
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'roommessages': roommessages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request):
    context = {}
    return render(request, 'base/profile.html', context)

def createTopic(request):
    tooopic = TopicForm()
    if request.method == 'POST':
        tooopic = TopicForm(request.POST)
        if tooopic.is_valid():
            room =  tooopic.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('Home')
    context = {'form': tooopic}
    return render(request, 'base/createTopic.html', context)


@login_required(login_url='/loginuser')
def createRoom(request):
    form  = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room =  form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('Home')
    context = {'form': form}
    return render(request, 'base/roomform.html', context)

@login_required(login_url='/loginuser')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
     
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')
    context = {'form': form}
    return render(request, 'base/roomform.html', context)

@login_required(login_url='/loginuser')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        room.delete()
        return redirect('Home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='/loginuser')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        message.delete()
        return redirect('Home')
    return render(request, 'base/delete.html', {'obj': message})

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('Home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Username Does not exist')
   
    context = {'page': page}
    return render(request, 'base/loginRegister.html', context)


def logoutuser(request):
    logout(request)   #delete the Token
    return redirect('Home')


def registerpage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'An error occur during registrtion')
    return render(request, 'base/loginRegister.html', {'form':form})

