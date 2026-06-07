from django.urls import path
from . import views

# REQUIRED configuration token mapping for isolating multi-app namespace environments
app_name = 'DjangoApp'  

urlpatterns = [
    path('', views.index, name='index'),
]