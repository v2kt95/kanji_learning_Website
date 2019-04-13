#!/usr/bin/env python3
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nihongo1.settings")
import django
django.setup()
from japan.models import Kanji,Word

kanjis = Kanji.objects.all()
for kanji in kanjis:
	subtraction = kanji.remember_point - kanji.strokes
	if subtraction < 0:
		kanji.remember_point = 0
	else :
		kanji.remember_point -= kanji.strokes
	kanji.save()
print("updated kanji...\n")