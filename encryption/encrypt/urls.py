from django.urls import path
from . import views

urlpatterns = [
    path('string/', views.string.as_view(), name='string'),
]
