import datetime

from django.db import models
from django.utils import timezone


class Kanji(models.Model):
    kanji = models.CharField(max_length=200)
    kanji_meaning = models.CharField(max_length=200)
    remember_point = models.IntegerField(default=0)
    strokes = models.IntegerField(default=0)
    def __str__(self):
        return self.kanji

class Word(models.Model):
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    hiragana_form = models.CharField(max_length=200)
    kanji_form = models.CharField(max_length=200)
    meaning_form = models.CharField(max_length=200)
    priority = models.IntegerField(default=0)
    remember_score = models.IntegerField(default=0)
    def __str__(self):
        return self.kanji_form