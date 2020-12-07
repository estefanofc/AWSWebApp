from django.urls import path, include

from .views import HomePageView, load, clear, query

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('load/', load, name='load'),
    path('clear/', clear, name='clear'),
    path('query/', query, name='query'),
]