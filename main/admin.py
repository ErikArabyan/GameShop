from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

admin.site.register(WelcomeText)
admin.site.register(Feature)
admin.site.register(Genres)
admin.site.register(Tags)
admin.site.register(GameDetails)
admin.site.register(CustomUser)
@admin.register(Game)
class GameDetailsForm(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class Group(DjangoGroup):
    class Meta:
        proxy = True

admin.site.unregister(DjangoGroup)

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass