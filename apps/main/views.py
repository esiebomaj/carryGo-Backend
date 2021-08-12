import random
import string

from django.db.models.signals import pre_save
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers
from .errors import InsufficientBalance


class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello Dashboad!'}
        return Response(content)


class PackageViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PackageSerializer
    queryset = models.Package.objects.all()


class TrackerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.TrackerSerializer
    queryset = models.Tracker.objects.all()

# Note that there is no transaction views because every
# transaction should be made via the wallet deposit and withdraw methods


class WalletDepositView(APIView):
    """this view should be used to deposit funds to a users wallet"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, amount):
        wallet = models.Wallet.objects.filter(pk=pk).first()
        wallet.deposit(amount)
        return Response({'message': 'deposit successfull'})


class WalletWithrawView(APIView):
    """this view should be used to withdraw funds from wallet"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, amount):
        wallet = models.Wallet.objects.filter(pk=pk).first()
        try:
            wallet.withdraw(amount)
            return Response({'message': 'withdraw successfull'})
        except InsufficientBalance:
            return Response({'message': 'insufficient balance'}, status=400)


class TranserView(APIView):
    """this view recieves a single package via post request and transer funds (package price)
     from owners account to carrier"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, amount):
        owner_wallet = models.Wallet.objects.filter(user=request.data['owner']).first()
        carrier_wallet = models.Wallet.objects.filter(user=request.data['carrier']).first()
        try:
            owner_wallet.transfer(carrier_wallet, amount)
            return Response({'message': 'transer successfull'})
        except InsufficientBalance:
            return Response({'message': 'insufficient balance'}, status=400)


def create_package_tracker(sender, instance, **kwargs):
    """signal to initialize a new tracker anythime the a package instance is saved"""
    if not sender.objects.filter(id=instance.id).exists():
        pin = generate_pin()
        instance.security_code = pin
        tracker = models.Tracker(is_confirmed=False)
        tracker.save()
        instance.tracker = tracker


pre_save.connect(receiver=create_package_tracker, sender=models.Package, dispatch_uid='create_package_tracker')


def generate_pin():
    """ generates pin for each new package being added to the database"""
    digits = string.digits
    pin = ''.join(random.choice(digits) for i in range(5))
    return pin
