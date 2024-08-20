from django.db import connection
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
        cursor = connection.cursor()

        cursor.execute(f"""
            SELECT courses_group.id, COUNT(users_subscription.user_id) AS user_count
            FROM courses_group
                LEFT JOIN users_subscription ON courses_group.course_id = users_subscription.course_id AND courses_group.id = users_subscription.group_id
            WHERE courses_group.course_id={instance.course.id}
            GROUP BY courses_group.id
            ORDER BY user_count, courses_group.id
            LIMIT 1;
        """)

        group_id, _ = cursor.fetchone()
        instance.group = Group.objects.get(id=group_id)
        instance.save()


@receiver(post_save, sender=Course)
def post_save_course(sender, instance: Course, created, **kwargs):
    '''Создание 10 групп после создания курса'''
    if created:
        Group.objects.bulk_create([Group(title=f'{num} group',
                                         course=instance) for num in range(1, 11)])



