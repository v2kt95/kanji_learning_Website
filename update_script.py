#!/usr/bin/env python3
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nihongo1.settings")
import django
django.setup()
from japan.models import Kanji,Word

kanjis = Kanji.objects.all()
for kanji in kanjis:
	if kanji.day_count == 1:
		kanji.day_count = kanji.day_down
		if kanji.level > 1:
			kanji.level -= 1
		kanji.save()
	else:
		print("before :",kanji.day_count)
		kanji.day_count -= 1		
		kanji.save()
		print("after :",kanji.day_count)
print("updated kanji...\n")