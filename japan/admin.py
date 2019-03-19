from django.contrib import admin

from .models import Kanji,Word

admin.site.register(Kanji)
admin.site.register(Word)