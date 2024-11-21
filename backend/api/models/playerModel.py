from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import transaction
import uuid


def getAvatarPath(self, filename):
    return str(self.pk) + '_avatar.png'
    # return f'avatars/{self.pk}/{"profile_image.png"}'

def getDefaultAvatar():
    return "static/avatars/poda.png" # default image should be in the static folder

class PlayerAdmin(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("You must provide an email address")
        if not username:
            raise ValueError("You must provide a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.status_profile = 1
        user.save(using=self._db)
        return user

class Player(AbstractBaseUser, PermissionsMixin):
    class STATUS(models.IntegerChoices):
        OFFLINE = 0, 'Offline'
        ONLINE = 1, 'Online'
        PLAYING = 2, 'Playing'

    is_42_user = models.BooleanField(default=False)

    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=24, blank=False, null=False, unique=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=False, null=False)
    password = models.CharField(max_length=250)
    avatar = models.CharField(max_length=255, null=True, blank=True, default=getDefaultAvatar)

    friends = models.ManyToManyField('self', blank=True)
    friend_count = models.IntegerField(default=0)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    tfaActive = models.BooleanField(default=False)
     

    elo = models.IntegerField(default=0)
    victories = models.PositiveIntegerField(default=0)
    defeats = models.PositiveIntegerField(default=0)
    games_played = models.PositiveIntegerField(default=0)
    tournaments_won = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    status_profile = models.IntegerField(choices=STATUS.choices, default=STATUS.OFFLINE)

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", null=True, blank=True)

    objects = PlayerAdmin() # custom user model manager

    USERNAME_FIELD = 'username'

    def __str__(self):
        if self:
            return self.username

    def get_formatted_date_joined(self):
        return self.date_joined.strftime('%Y-%m-%d')


    def get_status(self):
        return self.status_profile


    def get_friends(self):
        return self.friends.all()


    def get_friends_number(self):
        return self.friends.count()


    def are_friends(self, other_player):
        return self.friends.filter(pk=other_player.pk).exists()


    """Returns a group name based on the user's id to be used by Django Channels"""
    def group_name(self):
        id_str = str(self.id)
        return f'user_{id_str}'


    """Return the avatar filename"""
    def getAvatarFilename(self):
        return str(self.avatar)[str(self.avatar).index(f'{self.pk}/'):]


    def update_friend_count(self):
        self.friend_count = self.get_friends_number()
        self.save(update_fields=['friend_count'])


    def add_friend(self, account):
        if not self.are_friends(account):
            self.friends.add(account)
            self.update_friend_count()
            account.friends.add(self)
            account.update_friend_count()
            transaction.on_commit(lambda: self.update_friend_count())
            transaction.on_commit(lambda: account.update_friend_count())


    def remove_friends(self, account):
        if self.are_friends(account):
            self.friends.remove(account)
            self.update_friend_count()
            account.friends.remove(self)
            account.update_friend_count()
            transaction.on_commit(lambda: self.update_friend_count())
            transaction.on_commit(lambda: account.update_friend_count())


    def unfriend(self, removee):
        with transaction.atomic():
            self.remove_friends(removee)
            removee.remove_friends(self)

    def setDeco(self):
        print("je deco")
        self.status_profile = 0
        self.save()

