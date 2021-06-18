import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

logger = logging.getLogger('debug')

User = get_user_model()


@receiver(post_save, sender=User)
def signal_create_token(sender, instance, created, raw, **kwargs):
    '''
    Create a token (for auth in the rest-apis) when the user is created.
    '''
    if created and not raw:
        token = Token.objects.create(user=instance)
        logger.info(f'Token {token.key} for {instance.username}')
