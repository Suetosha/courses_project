from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription, Balance


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    def list(self, request, *args, **kwargs):
        courses = self.queryset.filter(is_available=True).exclude(subscription__user=request.user.id)
        serializer = self.get_serializer_class()(courses, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(**self.kwargs)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        user_balance = Balance.objects.get(user=request.user.id)
        course = Course.objects.get(pk=pk)

        is_user_subscribed = Subscription.objects.filter(user=request.user.id, course=pk)

        if is_user_subscribed:
            return Response({'error': 'User already subscribed'}, status=status.HTTP_400_BAD_REQUEST)

        total_user_bonuses = user_balance.bonus - course.price

        if total_user_bonuses < 0:
            return Response({'error': 'Not enough bonuses'}, status=status.HTTP_400_BAD_REQUEST)

        user_balance.bonus = total_user_bonuses
        user_balance.save()

        subscription = Subscription(user=request.user, course=course)
        subscription.save()

        serializer = SubscriptionSerializer(subscription)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )
