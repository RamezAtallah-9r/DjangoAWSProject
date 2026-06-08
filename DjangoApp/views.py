from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
from .models import *  # Explicit model imports are recommended in production paths

# provide html page for Login and regierstration
def index(request):
    return render(request, 'htmls/index.html')

# check if the user created or not and create new account
def create_user(request):
    if request.method == 'POST':

        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')
        date_of_birth= request.POST.get('date_of_birth')
        password= request.POST.get('password')
        confirm_password= request.POST.get('confirm_password')
        avatar=request.POST.get('avatar')
        user=check_user(email)
        if user:
            return redirect('DjangoApp:index')
        else:
            # After validation fails — add one message per error
            errors = User.objects.registration_validator(request.POST)
            if errors:
                for message in errors.values():
                    messages.error(request, message)
                    return redirect('DjangoApp:index')       # ← queues each error          # ← messages survive redirect
            else:
                user=create_users(first_name,last_name,email,date_of_birth,password,avatar)
                request.session['user_id']=user.id
            return redirect('DjangoApp:dashboard')
    
    else:
        return redirect('DjangoApp:index')
    
# check if the user exsist and if the password match or not
def login(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        password= request.POST.get('password')
        user=check_user(email)
        if user :
            loged_user=user_login(password,user)
            if loged_user:
                request.session['user_id']=user.id
                return redirect('DjangoApp:dashboard')
            else:
                return redirect('DjangoApp:index')

        else:
            return redirect('DjangoApp:index')
    else:
            return redirect('DjangoApp:index')    

# display the dashboard
def dashboard(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user=get_user(user_id)
        games= Game.objects.all()
    context={
        'user': user,
        'games':games,
    }
    return render(request, 'htmls/dashboard.html',context)

def create_game(request):
    if request.method == 'POST':
        game_name= request.POST.get('name')
        genre= request.POST.get('genre')
        release_date= request.POST.get('release_date')
        description= request.POST.get('description')

        if 'user_id' in request.session:
            user_id = request.session['user_id']
            user=get_user(user_id)
        game = create_games(game_name,genre,release_date,description,user)
        return redirect('DjangoApp:dashboard')
    else:
        return redirect('DjangoApp:dashboard')

def game_info(request, game_id):
    game=Game.objects.get(id=game_id)
    context={
        'game':game
    }
    return render(request,'htmls/display_game_info.html',context)

def edite_game_info(request,game_id):
    game=Game.objects.get(id=game_id)
    context={
        'game':game
    }
    return render(request, 'htmls/game_info.html',context)

def edite_game(request):
    if request.method == 'POST':
        game_id=request.POST.get('game_id')
        game_name= request.POST.get('name')
        genre= request.POST.get('genre')
        release_date= request.POST.get('release_date')
        description= request.POST.get('description')
        edite_games(game_id,game_name,genre,release_date,description)
        return redirect('DjangoApp:game_info',game_id)
    else:
        return redirect('DjangoApp:edite_game_info')
        

def logout(request):
    request.session.flush()
    return redirect('DjangoApp:index')