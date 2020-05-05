import datetime

from django.db import models


class Kanji(models.Model):
    kanji = models.CharField(max_length=200)
    kanji_meaning = models.CharField(max_length=200)
    strokes = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    kanji_explain = models.CharField(default="", max_length=500, null=True)
    other_information = models.CharField(default="", max_length=500, blank=True)
    review_time = models.DateTimeField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.kanji


class Word(models.Model):
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    hiragana_form = models.CharField(max_length=200)
    kanji_form = models.CharField(max_length=200)
    meaning_form = models.CharField(max_length=200)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.kanji_form


class TimeReset(models.Model):
    next_time = models.DateTimeField(null=True)
    kanji_list = models.CharField(default="", max_length=500, blank=True)
    kanji_original_count = models.IntegerField(default=0, blank=True)
