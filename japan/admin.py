from django.contrib import admin

from .models import Kanji, Word, TimeReset

admin.site.register(Kanji)
admin.site.register(Word)
admin.site.register(TimeReset)