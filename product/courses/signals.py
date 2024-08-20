from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from courses.models import Group, Course
from users.models import Subscription


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created:
        pass


@receiver(post_save, sender=Course)
def post_save_course(sender, instance: Course, created, **kwargs):
    '''Создание 10 групп после создания курса'''
    if created:
        Group.objects.bulk_create([Group(title=f'{num} group',
                                         course=instance) for num in range(1, 11)])
