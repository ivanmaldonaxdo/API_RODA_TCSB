import datetime
import pytz
from django.utils import timezone
from django.conf import settings
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.authtoken.models import Token


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self,key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Token Invalido')

        if not token.user.is_active:
            raise AuthenticationFailed('Usuario desactivado')

        utc_now=datetime.datetime.utcnow()
        utc_now=utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - settings.TOKEN_EXPIRED_AFTER_SECONDS:
            raise AuthenticationFailed('Token expirado')
        
        return token.user, token
