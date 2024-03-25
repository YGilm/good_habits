from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import Habit
from .paginators import HabitsPaginator
from .serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly


class HabitListCreateAPIView(ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitsPaginator

    def get_queryset(self):
        # Публичные привычки для всех, свои привычки для авторизованных
        if self.request.query_params.get('public', '0') == '1':
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Habit.objects.all()


class PublicHabitListAPIView(ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = HabitsPaginator
