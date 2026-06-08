from django.db import models
import re 
import bcrypt
# Create your models here.
class UserManager(models.Manager):

    def registration_validator(self, post_data):

        # Validates registration form data.
        # Receives request.POST dictionary.
        # Returns an errors dict — empty means all OK.
        errors = {}

        # ── First name ──────────────────────────────
        if len(post_data.get('first_name', '')) < 4:
            errors['first_name'] = 'First name must be at least 4 characters.'

        # ── Last name ───────────────────────────────
        if len(post_data.get('last_name', '')) < 4:
            errors['last_name'] = 'Last name must be at least 4 characters.'

        # ── Email (regex check) ─────────────────────
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, post_data.get('email', '')):
            errors['email'] = 'Please enter a valid email address.'

        # ── Password length ─────────────────────────
        if len(post_data.get('password', '')) < 8:
            errors['password'] = 'Password must be at least 8 characters.'

        # ── Password match ──────────────────────────
        if post_data.get('password') != post_data.get('confirm_password'):
            errors['confirm_password'] = 'Passwords do not match.'

        return errors          # empty dict = no errors

    def login_validator(self, post_data):
        """Validates login form data."""
        errors = {}

        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, post_data.get('email', '')):
            errors['email'] = 'Please enter a valid email address.'

        if len(post_data.get('password', '')) < 1:
            errors['password'] = 'Password is required.'

        return errors

    #-------------------------------------------
    # User Class
    #-------------------------------------------
class User(models.Model):
    first_name=models.CharField(max_length=250)
    last_name=models.CharField(max_length=250)
    email=models.CharField(max_length=250)
    date_of_birth=models.DateField()
    password=models.CharField(max_length=100)
    avatar=models.CharField(max_length=250)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    objects = UserManager()

    #-------------------------------------------
    # Game Class
    #-------------------------------------------
class Game(models.Model):
    game_name=models.CharField(max_length=250)
    genre=models.CharField(max_length=50)
    release_date=models.DateField()
    description=models.CharField(max_length=250)
    user=models.ForeignKey(User,related_name='games', on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    #-------------------------------------------
    # function for creating new users
    #-------------------------------------------
def create_users(first_name,last_name,email,date_of_birth,password,avatar):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    

    user=User.objects.create(first_name=first_name,
                             last_name=last_name,
                             email=email,
                             date_of_birth=date_of_birth,
                             password=hashed_password,
                             avatar=avatar )
    return user

    #-------------------------------------------
    # function for check if user exisest 
    #-------------------------------------------
def check_user(email):
    user=User.objects.filter(email=email)
    if user :
        return user[0]
    else :
        return False
    
def user_login(password,user):
    stored_hash=user.password
    entered_password =password

    # Both sides must be bytes — use .encode()
    password_matches = bcrypt.checkpw(
        entered_password.encode(),   # bytes of what user typed
        stored_hash.encode()         # bytes of the stored hash 
        )
    
    if password_matches:
        return user
    else:
        return False

def get_user(id):
    return User.objects.get(id=id)

def create_games(game_name,genre,release_date,description,user):
    game=Game.objects.filter(game_name=game_name)
    if game:
        return False
    else:
        game=Game.objects.create(
            game_name=game_name,
            genre=genre,
            release_date=release_date,
            description=description,
            user=user
        )
        return game


def edite_games(game_id,game_name,genre,release_date,description):
    game=Game.objects.get(id=game_id)
    game.game_name=game_name
    game.genre=genre
    game.release_date=release_date
    game.description=description
    game.save()
    return game