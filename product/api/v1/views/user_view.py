from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from api.v1.serializers.user_serializer import CustomUserSerializer, BalanceSerializer
from users.models import Balance

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = (permissions.IsAdminUser,)

    def list(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(self.queryset, many=True)
        return Response(serializer.data)


class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    http_method_names = ["get", "put", "head", "options"]
    permission_classes = (permissions.IsAdminUser,)

    def list(self, request, *args, **kwargs):
        serializer = BalanceSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, pk=None, **kwargs):
        body = request.data

        if 'amount' not in body:
            return Response({'error': 'Amount must be provided'})

        if type(body['amount']) is not int:
            return Response({'error': 'Amount must be integer'})

        if body['amount'] <= 0:
            return Response({'error': 'Amount must be greater than 0'})

        balance = Balance.objects.get(id=pk)
        balance.bonus += request.data['amount']
        balance.save()

        serializer = BalanceSerializer(balance)
        return Response(serializer.data)
