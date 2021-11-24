from rest_framework import status
from rest_framework.response import Response

from api.models import UserSubscription, User
from api.utils.email_sending import custom_send_email


def add_subscribe(subscriber: User, subscribe: int):
    """
    Подписаться на пользователя
    """
    user_subscription, create = UserSubscription.objects.get_or_create(subscriber_id=subscriber.pk,
                                                                       subscribe_id=subscribe)
    if create:
        try:
            subscribe_user = (UserSubscription.objects
                              .filter(subscriber_id=subscribe, subscribe_id=subscriber.pk)
                              .select_related('subscriber')
                              .only('subscriber__email', 'subscriber__first_name'))[0]
            custom_send_email('Match',
                              f'Вы понравились {subscriber.first_name}! '
                              f'Почта участника: {subscriber.email}',
                              [subscribe_user.subscriber.email])
            custom_send_email('Match',
                              f'Вы понравились {subscribe_user.subscriber.first_name}! '
                              f'Почта участника: {subscribe_user.subscriber.email}',
                              [subscriber.email])
        except IndexError:
            pass
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({
            'detail': 'You already subscribe'
        }, status=status.HTTP_400_BAD_REQUEST)


def check_subscribe(subscriber, subscribe):
    """
    Проверить наличие подписки
    """
    try:
        UserSubscription.objects.get(subscriber_id=subscriber.pk,
                                     subscribe_id=subscribe)
        return Response({
            'is_subscribed': True
        }, status=status.HTTP_200_OK)
    except UserSubscription.DoesNotExist:
        return Response({
            'is_subscribed': False
        }, status=status.HTTP_200_OK)


def delete_subscribe(subscriber, subscribe):
    try:
        UserSubscription.objects.get(subscriber_id=subscriber.pk,
                                     subscribe_id=subscribe).delete()
        return Response(status=status.HTTP_200_OK)
    except UserSubscription.DoesNotExist:
        return Response({
            'detail': 'You are not subscribe'
        }, status=status.HTTP_400_BAD_REQUEST)
