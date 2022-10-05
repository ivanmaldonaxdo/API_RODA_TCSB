from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id','email', 'password','name','telefono', 'role', 'is_active')
        

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('email', 'password','name','telefono', 'role')
    
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
