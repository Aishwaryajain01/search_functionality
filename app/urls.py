from django.urls import path
from . import views

urlpatterns = [
    path('suggest_terms/', views.suggest_terms, name='suggest_terms'),
    path('save_suggestion/', views.save_suggestion, name='save_suggestion'),
]
