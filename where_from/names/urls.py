from django.urls import path

from . import views

urlpatterns = [
    path('names/', views.name, name='name'),
    path('popular/', views.popular_names, name='popular_names'),
]
