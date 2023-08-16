from django.urls import path
from . import views

urlpatterns = [ # home est une fonction et on va inclure le dossier fact_app qui est une application le fichier urls.py du  projet principale
    path('', views.home, name='home'),
]
   