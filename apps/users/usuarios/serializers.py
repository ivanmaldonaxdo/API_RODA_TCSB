from rest_framework import serializers
from apps.users.models import User, Rol

#Serializador custom en caso de necesitarse
class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name')

#serializador par el metodo que genera el token
class UserTokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name')

#Serializador para la creacion de usuarios
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id','email', 'password','name','telefono', 'role', 'is_active')
        

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

#Serializador para metodo update del usuario
class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('email', 'password','name','telefono', 'role', 'master')
    
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    

#Serializador de contraseñas
class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    contraseña_actual = serializers.CharField(required=True)
    nueva_contraseña = serializers.CharField(required=True)


class UserRolSerializer(serializers.ModelSerializer):
    
  
    class Meta:
        model = User
        fields = ('email', 'role')
    
    def get_fields(self):
            fields = super().get_fields()
            if self.instance:
                fields["email"].read_only = True
            return fields
   