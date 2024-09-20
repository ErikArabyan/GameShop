from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class WelcomeText(models.Model):
    welcome = models.CharField('welcome', max_length=255, null=True)
    about = models.CharField('about', max_length=255, null=True)
    details = models.TextField('details', null=True)

class Feature(models.Model):
    feature = models.CharField('feature', max_length=255)
    img = models.ImageField('image')

class Genres(models.Model):
    Genre = models.CharField('Genre', max_length=64)
    top_category = models.BooleanField('top category')
    
    def __str__(self) -> str:
        return self.Genre
    
    class Meta():
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

class Game(models.Model):
    name = models.CharField('game name', max_length=64)
    GameGenre = models.ForeignKey(Genres, on_delete = models.CASCADE, related_name = 'Genres')
    price = models.IntegerField('game price')
    discount = models.IntegerField('price discount', default=0)
    trending = models.BooleanField('trending')
    most_played = models.BooleanField('most played')
    img = models.ImageField('image')
    def __str__(self):
        return f'{self.name}'
    
class CustomUser(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        blank=True,
        help_text=_("150 characters or fewer. Letters, digits and @/./+/-/_ only."),
    )
    email = models.EmailField(_("email address"), unique=True)
    img = models.ImageField('image', default='media/featured-02.png', upload_to='media/profile_images/')
    shopping_cart = models.ManyToManyField(Game, blank=True, related_name='shopping_cart')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class Subscribe(models.Model):
    email = models.EmailField('email', unique=True)

    def __str__(self):
        return self.email
    

class Tags(models.Model):
    Tag = models.CharField('Tag', max_length=64)
    def __str__(self) -> str:
        return self.Tag
    
    class Meta():
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class GameDetails(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE ,related_name='game_name')   
    game_ident = models.CharField('game_id', max_length=64)
    name = models.CharField('game name', max_length=64)
    about = models.TextField('about the game')
    genres = models.ManyToManyField(Genres, related_name='genres')
    tags = models.ManyToManyField(Tags, related_name='tags')

    def __str__(self) -> str:
            return self.name
    
    class Meta():
        verbose_name = 'Game Details'
        verbose_name_plural = 'Game Details'