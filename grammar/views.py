import os
from random import randint

from django.http import JsonResponse
from django.shortcuts import render
from openpyxl import load_workbook
from .models import Grammar, Sentence


# Create your views here.
def index(request):
    return render(request, 'grammar/index.html')


def load_excel_file(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    url = os.path.join(base_dir, 'kanji.xlsx')
    wb = load_workbook(url)
    sheet = wb.get_sheet_by_name('Sheet1')
    i = 2
    current_formula = sheet['A2'].value
    while sheet['F' + str(i)].value is not None:
        current_sentence = sheet['F' + str(i)].value
        if sheet['A' + str(i)].value is not None:
            current_formula = sheet['A' + str(i)].value
            is_existed_formula = Grammar.is_existed_grammar_by_formula(current_formula)
            if not is_existed_formula:
                formula = Grammar.create(sheet['A' + str(i)].value,
                                         sheet['B' + str(i)].value,
                                         sheet['C' + str(i)].value,
                                         sheet['D' + str(i)].value,
                                         sheet['E' + str(i)].value)
                formula.save()
            else:
                formula = Grammar.get_grammar_by_formula(current_formula)
            is_existed_sentence = Sentence.is_existed_sentence_by_grammar_and_content(formula, current_sentence)
            if not is_existed_sentence:
                sentence = Sentence.create(formula,
                                           sheet['F' + str(i)].value,
                                           sheet['G' + str(i)].value)
                sentence.save()
        else:
            formula = Grammar.get_grammar_by_formula(current_formula)
            is_existed_sentence = Sentence.is_existed_sentence_by_grammar_and_content(formula, current_sentence)
            if not is_existed_sentence:
                sentence = Sentence.create(formula,
                                           sheet['F' + str(i)].value,
                                           sheet['G' + str(i)].value)
                sentence.save()
        i += 1
    return JsonResponse({'result': current_formula})


def get_statistic_grammar(request):
    statistic_data = []
    for day_down in {2, 4, 6, 8}:
        day_down_data = []
        for lv in range(1, 6):
            grammar_count = Grammar.count_grammar(level=lv, day_down=day_down)
            day_down_data.append(grammar_count)
        statistic_data.append(day_down_data)
    return JsonResponse({'result': statistic_data})


def get_example(request):
    current_min_level = Grammar.get_grammars_by_conditions_and_order(order_by='level').first().level
    already_show_grammar = []
    if current_min_level == 5:
        data = dict(is_empty=True, alert='All Grammar is full level')
    else:
        if not request.session.get('grammar', False):
            grammar = Grammar.get_grammars_by_conditions_and_order(order_by='unit', level=current_min_level)
        else:
            already_show_grammar = request.session.get('grammar')
            grammar = Grammar.get_grammars_by_conditions_and_order(order_by='unit', level=current_min_level). \
                exclude(pk__in=already_show_grammar)
        if grammar.count() is 0:
            return JsonResponse(dict(is_empty=True, alert='Out of grammar'))

        total_grammar = grammar.count()
        random_index = randint(0, total_grammar - 1)
        sentence_belong_grammar = Sentence.get_sentence_by_conditions_and_order(order_by='?', grammar=grammar[random_index])
        already_show_grammar.append(grammar[random_index].pk)
        request.session['grammar'] = already_show_grammar
        print("grammar[random_index]: ", grammar[random_index])
        data = dict(grammar=list(grammar.values())[random_index], sentence=list(sentence_belong_grammar.values()),
                    is_empty=False)

        grammar_choose = grammar[random_index]
        grammar_choose.level += 1
        grammar_choose.day_count = grammar_choose.day_down
        grammar_choose.save()

    return JsonResponse(data)


def reset(request):
    request.session['grammar'] = []
    return JsonResponse(dict(response="ok"))


def get_list_remain_grammar(request):
    current_min_level = Grammar.get_grammars_by_conditions_and_order(order_by='level').first().level
    if not request.session.get('grammar', False):
        grammar = Grammar.get_grammars_by_conditions_and_order(order_by='unit', level=current_min_level).values()
    else:
        already_show_grammar = request.session.get('grammar')
        grammar = Grammar.get_grammars_by_conditions_and_order(order_by='unit', level=current_min_level).\
            exclude(pk__in=already_show_grammar).values()

    return JsonResponse({'result': list(grammar)})


def get_list_done_grammar(request):
    if not request.session.get('grammar', False):
        grammar = []
    else:
        already_show_grammar = request.session.get('grammar')
        grammar = list(Grammar.objects.filter(pk__in=already_show_grammar).values())
    return JsonResponse(dict(result=grammar))
