from django.contrib import admin

from core.models import Piece


@admin.register(Piece)
class PersonAdmin(admin.ModelAdmin):
    pass
