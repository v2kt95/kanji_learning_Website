#!/usr/bin/env python3
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nihongo1.settings")
import django

django.setup()
from japan.models import Kanji
from grammar.models import Grammar

kanjis = Kanji.objects.all()
grammars = Grammar.objects.all()
for kanji in kanjis:
    if kanji.day_count == 1:
        kanji.day_count = kanji.day_down
        if kanji.level > 1:
            kanji.level -= 1
        kanji.save()
    else:
        kanji.day_count -= 1
        kanji.save()

for grammar in grammars:
    if grammar.day_count == 1:
        grammar.day_count = grammar.day_down
        if grammar.level > 1:
            grammar.level -= 1
        grammar.save()
    else:
        print("before :", grammar.day_count)
        grammar.day_count -= 1
        grammar.save()
        print("after :", grammar.day_count)
print("updated kanji, grammar...\n")
