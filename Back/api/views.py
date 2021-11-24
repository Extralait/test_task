from decimal import Decimal

from django.db.models import Q
from djoser.permissions import CurrentUserOrAdmin
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import User, Distance
from api.permissions import NoBody
from api.serializers import UserSerializer, UserDetailsSerializer, CurrentUserDetailsSerializer, DistanceSerializer
from api.services.subscribers import check_subscribe, add_subscribe, delete_subscribe
from api.utils.field_transformation import get_no_files_fields


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 60
    page_size_query_param = 'page_size'
    max_page_size = 60


class DistanceViewset(viewsets.ModelViewSet):
    queryset = Distance.objects.all()
    serializer_class = DistanceSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = User.objects.all()
    filter_fields = get_no_files_fields(User)
    ordering_fields = filter_fields

    def _is_current_user(self):
        detail_user_pk = self.kwargs.get('pk')
        current_user_pk = self.request.user.pk
        return int(detail_user_pk) == current_user_pk

    def filter_queryset(self, queryset):
        user = self.request.user
        distance = self.request.query_params.get('distance')
        if distance:
            queryset = queryset.filter(
                Q(user_1__distance__lte=Decimal(str(distance))) |
                Q(user_2__distance__lte=Decimal(str(distance))),
            ).filter(~Q(pk=user.pk))
            print(queryset)
        return queryset

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        elif self.action in ['destroy', 'create']:
            permission_classes = (NoBody,)
        else:
            permission_classes = (CurrentUserOrAdmin,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Класс сериализатора
        """
        if self.detail:
            if self._is_current_user():
                serializer_class = CurrentUserDetailsSerializer
            else:
                serializer_class = UserDetailsSerializer
        else:
            serializer_class = UserSerializer

        return serializer_class

    @action(detail=True, methods=['get'], name='Match', permission_classes=(IsAuthenticated,))
    def match(self, request, **kwargs):
        """
        Проверка подписки участника
        """
        if self._is_current_user():
            return Response({
                'detail': 'Impossible to match to yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return check_subscribe(subscribe=int(self.kwargs.get('pk')),
                                   subscriber=self.request.user)

    @match.mapping.post
    def add_subscribe(self, request, **kwargs):
        """
        Создание подписки участника
        """
        if self._is_current_user():
            return Response({
                'detail': 'Impossible to add match to yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return add_subscribe(subscribe=int(self.kwargs.get('pk')),
                                 subscriber=self.request.user)

    @match.mapping.delete
    def delete_subscribe(self, request, **kwargs):
        """
        Удаление подписки участника
        """
        if self._is_current_user():
            return Response({
                'detail': 'Impossible delete to match to yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return delete_subscribe(subscribe=int(self.kwargs.get('pk')),
                                    subscriber=self.request.user)
