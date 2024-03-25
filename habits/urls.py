from habits.apps import HabitsConfig

from django.urls import path
from .views import HabitListCreateAPIView, HabitDetailAPIView, PublicHabitListAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/', HabitListCreateAPIView.as_view(), name='habit-list'),
    path('habits/<int:pk>/', HabitDetailAPIView.as_view(), name='habit-detail'),
    path('habits/public/', PublicHabitListAPIView.as_view(), name='public-habit-list'),
]
