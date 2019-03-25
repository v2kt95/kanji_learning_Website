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
    print(request.session['average_strokes'])
    return render(request, 'japan/index.html', context)

def get_word(request):
    is_priority_word = request.GET.get('priority', '')
    if is_priority_word == "true":
        priority_list = [1]
    else:
        priority_list = [1,0]
    # print(priority_list)
    if request.session.get('kanji', False) == False:
        already_show_kanji = []
        word = Word.objects.select_related('kanji').filter(kanji__remember_point__lte=0).filter(priority__in=priority_list).order_by("?").first()
        print(word)
    else:
        already_show_kanji = request.session.get('kanji')
        word = Word.objects.select_related('kanji').filter(kanji__remember_point__lte=0).filter(priority__in=priority_list).exclude(pk__in=already_show_kanji).order_by("?").first()
        print(word)
    # print(already_show_kanji)
    if word is None:
        data = {'is_empty': True}
    else:
        already_show_kanji.append(word.pk)
        request.session['kanji'] = already_show_kanji
        kanji = word.kanji
        data = {'kanji_meaning': kanji.kanji_meaning, 'kanji': kanji.kanji, 'hiragana_form': word.hiragana_form, 'kanji_form': word.kanji_form, 'meaning_form': word.meaning_form, 'is_empty': False}
        kanji.remember_point += request.session['average_strokes']
        kanji.save()
    return JsonResponse(data)

def reset(request):
    request.session['kanji'] = []
    return JsonResponse({'response': "ok"})

def mark_word(request):
    hiragana_word = request.GET.get('word', '')
    mark_word = Word.objects.filter(hiragana_form=hiragana_word).first()
    if mark_word is None:
        data = {'result': "failure"}
    else:
        kanji = mark_word.kanji
        kanji.remember_point -= round(request.session['average_strokes']/2)
        kanji.save()
        data = {'result': "success"}
    return JsonResponse(data) 

def load_excel_file(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    url = os.path.join(BASE_DIR, 'kanji.xlsx')
    wb = load_workbook(url)
    # wb = load_workbook('C://Users//vuongdv3//Desktop//kanji.xlsx')
    sheet = wb.get_sheet_by_name('Sheet1')
    # current_kanji = sheet['A2'].value
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
    is_priority_word = request.GET.get('priority', '')
    if is_priority_word == "true":
        priority_list = [1]
    else:
        priority_list = [1,0]

    if request.session.get('kanji', False) == False:
        already_show_kanji = []
        word = Word.objects.select_related('kanji').filter(kanji__remember_point__lte=0).filter(priority__in=priority_list).values()
    else:
        already_show_kanji = request.session.get('kanji')
        word = Word.objects.select_related('kanji').filter(kanji__remember_point__lte=0).filter(priority__in=priority_list).exclude(pk__in=already_show_kanji).values()
    return JsonResponse({'result': list(word)})

def get_list_done_word(request):
    if request.session.get('kanji', False) == False:
        already_show_kanji = []
        word = []
    else:
        already_show_kanji = request.session.get('kanji')
        word = list(Word.objects.filter(pk__in=already_show_kanji).values())
    return JsonResponse({'result': word})

def get_list_old_word(request):
    word = Kanji.objects.filter(remember_point__lte=-20).values()
    return JsonResponse({'result': list(word)})

