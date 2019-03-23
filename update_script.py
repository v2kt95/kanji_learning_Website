#!/usr/bin/env python3
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nihongo1.settings")
import django
django.setup()
from japan.models import Kanji,Word

kanjis = Kanji.objects.get(id=153)
kanjis.remember_point -= kanjis.strokes
kanjis.save()
# for kanji in kanjis:
# 	kanji.remember_point -= kanji.strokes
# 	kanji.save()
print("updated kanji...\n")