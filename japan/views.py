import os
from random import randint

from django.http import JsonResponse
from django.shortcuts import render
from openpyxl import load_workbook

from .models import Kanji, Word, TimeReview


def index(request):
    kanji_list = Kanji.objects.all()
    context = {'kanji_list': kanji_list}
    return render(request, 'japan/index.html', context)


def get_statistic_kanji(request):
    statistic_data = []
    for day_down in [2, 4, 6, 8]:
        day_down_data = []
        for lv in range(1,6):            
            kanji_num = Kanji.objects.filter(level=lv).filter(day_down=day_down).count()
            day_down_data.append(kanji_num)
        statistic_data.append(day_down_data)
    return JsonResponse({'result': statistic_data})


def get_word(request):
    current_min_level = Kanji.objects.order_by("level")[0].level
    already_show_kanji = []
    if current_min_level == 5:
        data = {'is_empty': True, 'alert' : 'All Kanji is full level'}
    else:
        if not request.session.get('kanji', False):
            kanji = Kanji.objects.filter(level=current_min_level).order_by('-strokes')            
        else:
            already_show_kanji = request.session.get('kanji')
            kanji = Kanji.objects.filter(level=current_min_level).exclude(pk__in=already_show_kanji).order_by('-strokes')
        if kanji.count() == 0:
            TimeReview.objects.all().delete()
            TimeReview().save()
            return JsonResponse({'is_empty': True, 'alert' : 'Out of kanji'})

        # total_kanji = kanji.count()
        # random_index = randint(0, total_kanji - 1)
        word_belong_kanji = Word.objects.filter(kanji=kanji[0]).order_by("priority")
        already_show_kanji.append(kanji[0].pk)
        request.session['kanji'] = already_show_kanji
        data = {'kanji': list(kanji.values())[0], 'word': list(word_belong_kanji.values()), 'is_empty': False}
        kanji_first = kanji[0]
        kanji_first.level += 1
        kanji_first.day_count = kanji_first.day_down
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
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    url = os.path.join(base_dir, 'kanji.xlsx')
    wb = load_workbook(url)
    sheet = wb.get_sheet_by_name('Sheet1')
    i = 2
    current_kanji = sheet['A2'].value
    while sheet['C' + str(i)].value is not None:
        current_word = sheet['C'+str(i)].value
        if sheet['A' + str(i)].value is not None:
            current_kanji = sheet['A'+str(i)].value
            is_existed_kanji = Kanji.objects.filter(kanji=current_kanji).count() > 0
            if not is_existed_kanji:
                kanji = Kanji(kanji=sheet['A'+str(i)].value,kanji_meaning=sheet['B'+str(i)].value,strokes=sheet['F'+str(i)].value, kanji_explain=sheet['G'+str(i)].value)
                kanji.save()
            else:
                kanji = Kanji.objects.filter(kanji=current_kanji).first()            
            is_existed_word = Word.objects.filter(kanji=kanji).filter(hiragana_form=current_word).count() > 0
            if not is_existed_word:
                word = Word(kanji=kanji,hiragana_form=sheet['C'+str(i)].value,kanji_form=sheet['D'+str(i)].value, meaning_form=sheet['E'+str(i)].value, priority=1)
                word.save()            
        else:            
            kanji = Kanji.objects.filter(kanji=current_kanji).first()
            is_existed_word = Word.objects.filter(kanji=kanji).filter(hiragana_form=current_word).count() > 0
            if not is_existed_word:
                word = Word(kanji=kanji, hiragana_form=sheet['C'+str(i)].value,kanji_form=sheet['D'+str(i)].value, meaning_form=sheet['E'+str(i)].value)
                word.save()
        i += 1
    return JsonResponse({'result': current_kanji})


def get_list_remain_word(request):
    current_min_level = Kanji.objects.order_by("level")[0].level
    if not request.session.get('kanji', False):
        kanji = Kanji.objects.filter(level=current_min_level).order_by("-strokes").values()
    else:
        already_show_kanji = request.session.get('kanji')
        kanji = Kanji.objects.filter(level=current_min_level).exclude(pk__in=already_show_kanji).order_by("-strokes").values()

    return JsonResponse({'result': list(kanji)})


def get_list_done_word(request):
    if not request.session.get('kanji', False):
        kanji = []
    else:
        already_show_kanji = request.session.get('kanji')
        kanji = list(Kanji.objects.filter(pk__in=already_show_kanji).values())
    return JsonResponse({'result': kanji})
