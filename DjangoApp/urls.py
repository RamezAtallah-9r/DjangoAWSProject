from django.urls import path
from . import views

# REQUIRED configuration token mapping for isolating multi-app namespace environments
app_name = 'DjangoApp'  

urlpatterns = [
    path('', views.index, name='index'),
    path('create_user', views.create_user, name='create_user'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('create_game', views.create_game, name='create_game'),
    path('game_info/<int:game_id>', views.game_info, name='game_info'),
    path('edite_game_info/<int:game_id>', views.edite_game_info, name='edite_game_info'),
    path('edite_game', views.edite_game, name='edite_game'),
    path('logout', views.logout, name='logout'),
]