import datetime

from django.db import models
from django.utils import timezone


class Kanji(models.Model):
    kanji = models.CharField(max_length=200)
    kanji_meaning = models.CharField(max_length=200)
    remember_point = models.IntegerField(default=0)
    strokes = models.IntegerField(default=0)
    level = models.IntegerField(default=4)
    day_down = models.IntegerField(default=1)
    day_count = models.IntegerField(default=1)

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        if self.strokes <=5 :
            self.day_down = 8
        elif self.strokes <=8:
            self.day_down = 6
        elif self.strokes <= 11:
            self.day_down = 4
        else:
            self.day_down = 2
            
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

class TimeReview(models.Model):
    """docstring for TimeReview"""
    LastTimeReview = models.DateTimeField(default=datetime.datetime.now, blank=True)
    NextTimeReview = models.DateTimeField(blank=True)

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.NextTimeReview = self.LastTimeReview+datetime.timedelta(minutes=30)
