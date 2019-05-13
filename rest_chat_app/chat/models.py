from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import datetime

from django.core.cache import cache


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else:
            return False


class Message(models.Model):
    # sender is used to identify the sender of the message
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)  #  message is a CharField to store the text.
    timestamp = models.DateTimeField(auto_now_add=True) # timestamp stores the date and time of creation of message
    is_read = models.BooleanField(default=False) # is_read keeps track if the message is read or not.

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)


