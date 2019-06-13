from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Kanji,Word,TimeReview
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
import json
from openpyxl import load_workbook
import os
import datetime
from django.db.models import Avg, Max, Min, Sum

def index(request):
    kanji_list = Kanji.objects.all()
    context = {'kanji_list': kanji_list}
    return render(request, 'japan/index.html', context)

def get_statistic_kanji(request):
    statistic_data = []
    for daydown in range(1,5):
        daydown_data = []
        for lv in range(1,6):            
            kanji_num = Kanji.objects.filter(level=lv).filter(day_down=daydown).count()
            daydown_data.append(kanji_num)
        statistic_data.append(daydown_data)
    return JsonResponse({'result': statistic_data})

def getWorsd2(request):
    current_min_level = Kanji.objects.order_by("level")[0].level
    review_time = TimeReview.objects.all()[0].NextTimeReview.replace(tzinfo=None)
    current_time = datetime.datetime.now()
    if current_min_level == 5:
        data = {'is_empty': True, 'alert' : 'All Kanji is full level'}
    # elif current_time < review_time:
    #     local_time_review = review_time + datetime.timedelta(hours=7)
    #     review_time_str = local_time_review.strftime("%d-%b-%Y (%H:%M:%S)")
    #     data = {'is_empty': True, 'alert' : 'Please wait until ' + review_time_str + ' to continue'}
    else:
        if request.session.get('kanji', False) == False:
            alreadyShowKanji = []        
            kanji = Kanji.objects.filter(level=current_min_level).order_by('?')
        else:
            alreadyShowKanji = request.session.get('kanji')
            kanji = Kanji.objects.filter(level=current_min_level).exclude(pk__in=alreadyShowKanji).order_by('?')

        if kanji.count() == 0:
            TimeReview.objects.all().delete()
            TimeReview().save()
            return JsonResponse({'is_empty': True, 'alert' : 'Out of kanji'})

        wordBelongKanji = Word.objects.filter(kanji=kanji[0]).order_by("priority")
        alreadyShowKanji.append(kanji[0].pk)
        request.session['kanji'] = alreadyShowKanji
        data = {'kanji': list(kanji.values())[0], 'word': list(wordBelongKanji.values()), 'is_empty': False}
        kanji_first = kanji[0]
        kanji_first.level += 1
        kanji_first.save()

    return JsonResponse(data)

def reset(request):
    request.session['kanji'] = []
    return JsonResponse({'response': "ok"})

def mark_word(request):
    kanji = request.GET.get('word', '')
    mark_kanji = Kanji.objects.filter(kanji=kanji).first()
    if mark_kanji is None:
        data = {'result': "failure"}
    else:
        mark_kanji.level -= 1
        mark_kanji.save()
        data = {'result': "success"}

    return JsonResponse(data)

def load_excel_file(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    url = os.path.join(BASE_DIR, 'kanji.xlsx')
    wb = load_workbook(url)
    sheet = wb.get_sheet_by_name('Sheet1')
    i = 2
    current_kanji = sheet['A2'].value
    while sheet['C'+str(i)].value != None:
        current_word = sheet['C'+str(i)].value
        if sheet['A'+str(i)].value != None:            
            current_kanji = sheet['A'+str(i)].value
            is_existed_kanji = Kanji.objects.filter(kanji=current_kanji).count() > 0
            if not is_existed_kanji:
                kanji = Kanji(kanji=sheet['A'+str(i)].value,kanji_meaning=sheet['B'+str(i)].value,strokes=sheet['F'+str(i)].value)
                kanji.save()
            else:
                kanji = Kanji.objects.filter(kanji=current_kanji).first()            
            is_existed_word = Word.objects.filter(kanji=kanji).filter(hiragana_form=current_word).count() > 0
            if not is_existed_word:
                word = Word(kanji=kanji,hiragana_form=sheet['C'+str(i)].value,kanji_form=sheet['D'+str(i)].value,meaning_form=sheet['E'+str(i)].value,priority=1)
                word.save()            
        else:            
            kanji = Kanji.objects.filter(kanji=current_kanji).first()
            is_existed_word = Word.objects.filter(kanji=kanji).filter(hiragana_form=current_word).count() > 0
            if not is_existed_word:
                word = Word(kanji=kanji,hiragana_form=sheet['C'+str(i)].value,kanji_form=sheet['D'+str(i)].value,meaning_form=sheet['E'+str(i)].value)
                word.save()
        i += 1
    return JsonResponse({'result': current_kanji})

def get_list_remain_word(request):
    current_min_level = Kanji.objects.order_by("level")[0].level
    if request.session.get('kanji', False) == False:
        alreadyShowKanji = []
        kanji = Kanji.objects.filter(level=current_min_level).order_by("-strokes").values()
    else:
        alreadyShowKanji = request.session.get('kanji')
        kanji = Kanji.objects.filter(level=current_min_level).exclude(pk__in=alreadyShowKanji).order_by("-strokes").values()

    return JsonResponse({'result': list(kanji)})

def get_list_done_word(request):
    if request.session.get('kanji', False) == False:
        alreadyShowKanji = []
        kanji = []
    else:
        alreadyShowKanji = request.session.get('kanji')
        kanji = list(Kanji.objects.filter(pk__in=alreadyShowKanji).values())

    return JsonResponse({'result': kanji})
