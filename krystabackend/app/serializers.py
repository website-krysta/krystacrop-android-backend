from rest_framework import serializers
from .models import user,orders



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields = '__all__'