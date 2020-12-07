from django.urls import path, include

from .views import HomePageView, load, clear

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('load/', load, name='load'),
    path('clear/', clear, name='clear'),
]