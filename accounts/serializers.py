from rest_framework import serializers
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import *
from chat.models import *

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_null=False,)
    password = serializers.CharField(required=True, allow_null=False)
    
    def authenticate(self, username=None, password=None, email=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = User.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True,allow_null=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name' , 'last_name', 'id')
        extra_kwargs = {
			'first_name': {'required': True},
			'last_name': {'required': True},
			'email': {'required': True},
			'password': {'required': True},
		}

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data['email']
        try:
            user = super(UserSerializer, self).create(validated_data)
        except:
            raise email + " already exists"

        user.set_password(validated_data['password'])
        user.save()
        chatRoom = ChatRoom.objects.create(
			type="SELF", name=user.first_name + user.last_name
		)
        chatRoom.member.add(user.id)
        return user