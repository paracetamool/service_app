from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch

from .models import Subscription
from clients.models import Client
from .serializers import SubscriptionSerializers


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', 
        queryset=Client.objects.all().select_related("user").only('company_name', 'user__email'))
    )
    serializer_class = SubscriptionSerializers
