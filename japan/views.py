from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Kanji,Word
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
import json
from openpyxl import load_workbook
import os
from django.db.models import Avg, Max, Min, Sum

def index(request):
    kanji_list = Kanji.objects.all()
    context = {'kanji_list': kanji_list}
    request.session['average_strokes'] = get_average_strokes()
    # print(request.session['average_strokes'])
    return render(request, 'japan/index.html', context)

def getWorsd2(request):
    priorityList = [1]
    if request.session.get('kanji', False) == False:
        alreadyShowKanji = []
        kanji = Kanji.objects.filter(remember_point__lte=0)
    else:
        alreadyShowKanji = request.session.get('kanji')
        kanji = Kanji.objects.filter(remember_point__lte=0).exclude(pk__in=alreadyShowKanji)
    if kanji is None:
        data = {'is_empty': True}
    else:
        wordBelongKanji = Word.objects.filter(kanji=kanji[0]).order_by("priority")
        alreadyShowKanji.append(kanji[0].pk)
        request.session['kanji'] = alreadyShowKanji
        data = {'kanji': list(kanji.values())[0], 'word': list(wordBelongKanji.values()), 'is_empty': False}
        kanji[0].remember_point += request.session['average_strokes']
        kanji[0].save()
    return JsonResponse(data)

def reset(request):
    request.session['kanji'] = []
    return JsonResponse({'response': "ok"})

def mark_word(request):
    kanji = request.GET.get('word', '')
    mark_kanji = Kanji.objects.filter(kanji=kanji).first()
    # mark_word = Word.objects.filter(hiragana_form=hiragana_word).first()
    if mark_kanji is None:
        data = {'result': "failure"}
    else:
        # kanji = mark_word.kanji
        mark_kanji.remember_point -= round(request.session['average_strokes']/2)
        mark_kanji.save()
        data = {'result': "success"}
    return JsonResponse(data)

def load_excel_file(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    url = os.path.join(BASE_DIR, 'kanji.xlsx')
    wb = load_workbook(url)
    sheet = wb.get_sheet_by_name('Sheet2')
    i = 2
    current_kanji = sheet['A2'].value
    while sheet['C'+str(i)].value != None:
        if sheet['A'+str(i)].value != None:
            current_kanji = sheet['A'+str(i)].value
            kanji = Kanji(kanji=sheet['A'+str(i)].value,kanji_meaning=sheet['B'+str(i)].value,strokes=sheet['F'+str(i)].value)
            kanji.save()
            word = Word(kanji=kanji,hiragana_form=sheet['C'+str(i)].value,kanji_form=sheet['D'+str(i)].value,meaning_form=sheet['E'+str(i)].value,priority=1)
            word.save()
        else:
            kanji = Kanji.objects.filter(kanji=current_kanji).first()
            word = Word(kanji=kanji,hiragana_form=sheet['C'+str(i)].value,kanji_form=sheet['D'+str(i)].value,meaning_form=sheet['E'+str(i)].value)
            word.save()
        i += 1
    return JsonResponse({'result': current_kanji})

def get_average_strokes():
    kanjis = Kanji.objects.all()
    return round(kanjis.aggregate(Avg('strokes'))["strokes__avg"])

def get_list_remain_word(request):
    # is_priority_word = request.GET.get('priority', '')
    # priority_list = [1]

    if request.session.get('kanji', False) == False:
        already_show_kanji = []
        # word = Word.objects.select_related('kanji').filter(kanji__remember_point__lte=0).filter(priority__in=priority_list).values()
        kanji = Kanji.objects.filter(remember_point__lte=0).values()
    else:
        already_show_kanji = request.session.get('kanji')
        # word = Word.objects.select_related('kanji').filter(kanji__remember_point__lte=0).filter(priority__in=priority_list).exclude(pk__in=already_show_kanji).values()
        kanji = Kanji.objects.filter(remember_point__lte=0).exclude(pk__in=already_show_kanji).values()
    return JsonResponse({'result': list(kanji)})

def get_list_done_word(request):
    if request.session.get('kanji', False) == False:
        already_show_kanji = []
        word = []
    else:
        already_show_kanji = request.session.get('kanji')
        word = list(Kanji.objects.filter(pk__in=already_show_kanji).values())
    return JsonResponse({'result': word})

def get_list_old_word(request):
    word = Kanji.objects.filter(remember_point__lte=-10).values()
    # for w in word:
    #     w.remember_point=-7
    #     w.save()
    return JsonResponse({'result': list(word)})

def toJSON(self):
    import simplejson
    return simplejson.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))