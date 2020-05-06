import os

from django.http import JsonResponse
from django.shortcuts import render
from openpyxl import load_workbook
from datetime import datetime, timedelta, timezone

from .models import Kanji, Word, TimeReset


def index(request):
    time_reset, is_success = TimeReset.objects.get_or_create(pk=1)
    context = {'kanji_list': []}
    if time_reset.next_time is None or time_reset.next_time < datetime.now(timezone.utc):
        current_min_level = Kanji.objects.order_by("level")[0].level
        time_now = datetime.now(timezone.utc)
        review_kanji = Kanji.objects.filter(review_time__gt=time_now)
        if current_min_level == 5:
            data = [kanji.id for kanji in review_kanji]
        else:
            min_level_kanji = Kanji.objects.filter(level=current_min_level)
            data = [kanji.id for kanji in min_level_kanji] + [kanji.id for kanji in review_kanji]
        time_reset.kanji_list = ",".join([str(x) for x in data])
        time_reset.kanji_original_count = len(data)
    else:
        context = {'kanji_list': [], 'next_time': (time_reset.next_time + timedelta(hours=9)).strftime("%m/%d/%Y, %H:%M:%S")}
        time_reset.kanji_list = ""
        time_reset.kanji_original_count = 0
    time_reset.save()
    return render(request, 'japan/index.html', context)


def get_statistic_kanji(request):
    statistic_data = []
    for lv in range(1, 6):
        kanji_num = Kanji.objects.filter(level=lv).count()
        statistic_data.append(kanji_num)
    return JsonResponse({'result': statistic_data})


def get_word(request):
    time_reset, is_success = TimeReset.objects.get_or_create(pk=1)
    try:
        if not time_reset.kanji_list:
            count = time_reset.kanji_original_count
            time_reset.next_time = datetime.now(timezone.utc) + timedelta(minutes=count)
            time_reset.kanji_original_count = 0
            time_reset.kanji_list = ''
            time_reset.save()
            return JsonResponse({'is_empty': True, 'alert': 'Out of kanji'})
        else:
            kanji_ids = time_reset.kanji_list.split(',')
            kanji_id = kanji_ids.pop(0)
            time_reset.kanji_list = ','.join(kanji_ids)
            time_reset.save()

            kanji = Kanji.objects.get(pk=int(kanji_id))
            word_belong_kanji = Word.objects.filter(kanji=kanji).order_by("-priority")
            kanji_dict = kanji.__dict__
            kanji_dict.pop('_state', None)
            data = {'kanji': kanji_dict, 'word': list(word_belong_kanji.values()), 'is_empty': False}
            return JsonResponse(data)
    except IndexError:
        return JsonResponse({'is_empty': True, 'alert': 'Out of kanji'})


def save_kanji_score(request):
    try:
        kanji_id = request.GET.get('id', None)
        correct_count = request.GET.get('correct_count', None)
        kanji = Kanji.objects.get(pk=kanji_id)
        kanji_word_count = Word.objects.filter(kanji=kanji).count()
        if int(correct_count) == int(kanji_word_count) and kanji.level < 5:
            kanji.level += 1
            if kanji.level == 5:
                kanji.review_time = datetime.now() + timedelta(days=7)
        else:
            if kanji.level == 5:
                kanji.review_time = datetime.now() + timedelta(days=3)
        kanji.save()
        return JsonResponse({'response': "success"})
    except:
        return JsonResponse({'response': "failure"})


def load_excel_file(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    url = os.path.join(base_dir, 'kanji.xlsx')
    wb = load_workbook(url)
    sheet = wb.get_sheet_by_name('Sheet1')
    i = 2

    new_kanji = sheet['A2'].value
    while sheet['C' + str(i)].value is not None:
        current_word = sheet['C' + str(i)].value

        if sheet['A' + str(i)].value is not None:
            new_kanji = sheet['A' + str(i)].value
            is_priority_word = True
        else:
            is_priority_word = False

        current_kanji, _is_create_kanji = Kanji.objects.get_or_create(kanji=new_kanji)
        current_kanji.kanji_meaning = format_text(sheet['B' + str(i)].value, current_kanji.kanji_meaning)
        current_kanji.strokes = get_number(sheet['F' + str(i)].value, current_kanji.strokes)
        current_kanji.kanji_explain = format_text(sheet['G' + str(i)].value, current_kanji.kanji_explain)
        current_kanji.other_information = format_text(sheet['H' + str(i)].value, current_kanji.other_information)
        current_kanji.save()

        current_word, _is_create_word = Word.objects.get_or_create(kanji=current_kanji, hiragana_form=current_word)
        current_word.kanji_form = sheet['D' + str(i)].value.strip()
        current_word.meaning_form = sheet['E' + str(i)].value.strip()
        current_word.priority = 1 if is_priority_word else 0
        current_word.save()

        i += 1
    return JsonResponse({'result': 'success'})


def get_number(value, default_value):
    if isinstance(value, int):
        return value
    return default_value


def format_text(value, default_value):
    if not value:
        return default_value
    return value.strip()


def get_list_remain_word(request):
    time_reset, is_success = TimeReset.objects.get_or_create(pk=1)
    if not time_reset.kanji_list:
        return JsonResponse({'result': []})
    else:
        kanji_ids = time_reset.kanji_list.split(',')
        kanji_ids = [int(k) for k in kanji_ids]
        kanji_list = Kanji.objects.filter(pk__in=kanji_ids)
        return JsonResponse({'result': list(kanji_list.values())})


def divide_group(request):
    lv1_kanjis = Kanji.objects.filter(level=1)
    level = 1
    for i in range(len(lv1_kanjis)):
        if i > 75 and i <= 150:
            lv1_kanjis[i].level = 3
        elif i > 150:
            lv1_kanjis[i].level = 4
        else:
            lv1_kanjis[i].level = 1
        lv1_kanjis[i].save()
    return JsonResponse({'result': 'sucess'})