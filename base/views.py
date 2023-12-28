from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, Message, User
from .forms import RoomForm, NewUserForm, UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
ROOMS_PAGE = 10

def home(request):
  # request.GET get query in url ?q=...
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  # request get page number ex: ?page=2
  current_page = request.GET.get('page') if request.GET.get('page') != None else ''
  # query room LIKE %q%
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
  )
  
  room_count = len(rooms)
  p = Paginator(rooms, ROOMS_PAGE)
  try:
    page_obj = p.get_page(current_page)
  except PageNotAnInteger as e:
    page_obj = p.page(1)
  except EmptyPage:
    page_obj = p.page(p.num_pages)
  
  room_messages = Message.objects.filter(
    Q(room__topic__name__icontains=q) |
    Q(room__name__icontains=q) |
    Q(room__description__icontains=q)
  )
  # query topics in rooms
  topics = Topic.objects.all()[0:5]
  context = {
    'rooms': rooms,
    'topics': topics, 
    'room_count': room_count,
    'room_messages': room_messages,
    'q': q,
    'p': p,
    'page_obj': page_obj,
  }
  return render(request, 'base/home.html', context)



def room(request, id):
  room = Room.objects.get(id=id)
  room_messages = room.message_set.all().order_by('-created') # dash is desc
  participants = room.participants.all()
  if request.method == 'POST':
    message = Message.objects.create(
      user=request.user,
      room=room,
      message=request.POST.get('message')
    )
    room.participants.add(request.user)
    return redirect('room', id=room.id)
  context = {
    'room': room,
    'room_messages': room_messages,
    'participants': participants,
    }
  return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
  page = 'create'
  form = RoomForm()
  topics = Topic.objects.all()

  if request.method == 'POST':
    topic_name = request.POST.get('topics')
    topic_name = topic_name.lower().capitalize()
    topic, created = Topic.objects.get_or_create(name=topic_name)

    room = Room.objects.create(
      host=request.user,
      topic=topic,
      name=request.POST.get('name'),
      description=request.POST.get('description'),
    )
    room.participants.add(request.user)
    messages.success(request, 'You created the room successfully!')
    return redirect('home')

  context = {
    'form': form,
    'topics': topics,
    'page': page,
    }
  return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updatedRoom(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  topics = Topic.objects.all()
  if request.user != room.host:
    return HttpResponse('You are not allowed here!')

  if request.method == 'POST':
    topic_name = request.POST.get('topics')
    topic_name = topic_name.lower().capitalize()
    topic, created = Topic.objects.get_or_create(name=topic_name)
    room.name = request.POST.get('name')
    room.topic = topic
    room.description = request.POST.get('description')
    room.save()
    messages.success(request, 'You updated the room successfully!')
    return redirect('home')

  context = {
    'form': form,
    'topics': topics,
    'room': room,
    }
  return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
  room = Room.objects.get(id=pk)

  if request.user != room.host:
    return HttpResponse('You are not allowed here!')

  if request.method == "POST":
    room.delete()
    return redirect('home')
  return render(request, 'base/delete_room.html', {'obj': room})

def loginPage(request):
  page = 'login'

  # dont re-login
  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':
    email = request.POST.get('email').lower()
    password = request.POST.get('password')

    try: 
      user = User.objects.get(email=email)
    except:
      messages.error(request, message='User does not exist')

    user = authenticate(request, email=email, password=password)
    if user is not None:
      login(request, user=user)
      messages.success(request, 'You logged in successfully.')
      return redirect('home')
    else:
      messages.error(request, 'Username or password does not exist.')
  context = {'page': page}
  return render(request, 'base/login_register.html', context)

def logoutUser(request):
  logout(request)
  return redirect('home')

def registerPage(request):
  form = NewUserForm()
  if request.method == 'POST':
    form = NewUserForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      messages.success(request, message='You have created your account successfully!')
      return redirect('home')
    else:
      messages.error(request, message='An error occurred during registration')
  return render(request, 'base/login_register.html', {'form': form})

@login_required(login_url='login')
def deleteMessage(request, pk_room, pk):
  message = Message.objects.get(id=pk)

  if request.method == "POST":
    message.delete()
    return redirect('room', id=pk_room)
  return render(request, 'base/delete_room.html', {'obj': message})

def userProfile(request, pk):
  user = User.objects.get(id=pk)
  rooms = user.room_set.all()
  room_messages = user.message_set.all()
  room_count = rooms.count
  topics = Topic.objects.all()
  context = {
    'user': user,
    'rooms': rooms,
    'room_count': room_count,
    'room_messages': room_messages,
    'topics': topics,
  }

  return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateUser(request, pk):
  user = request.user
  form = UserForm(instance=user)
  if request.method == 'POST':
    form = UserForm(request.POST,request.FILES, instance=user)
    if form.is_valid():
      form.save()
      return redirect('user-profile', pk=user.id)
  context = {
    'form': form,
  }
  return render(request, 'base/update_user.html', context)

def topicsPage(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  topics = Topic.objects.filter(name__icontains=q)

  context = {
    'topics': topics,
  }
  return render(request, 'base/topics.html', context)

def activitiesPage(request):
  messages = Message.objects.all()
  context = {
    'messages': messages,
  }
  return render(request, 'base/activities.html', context)