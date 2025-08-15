from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = manageUser
        fields = '__all_'