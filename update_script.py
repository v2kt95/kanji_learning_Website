#!/usr/bin/env python3
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nihongo1.settings")
import django
django.setup()
from japan.models import Kanji,Word

kanjis = Kanji.objects.all()
for kanji in kanjis:
	kanji.remember_point -= kanji.strokes
	kanji.save()
print("updated kanji...\n")