from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('get_statistic_kanji', views.get_statistic_kanji, name='get_statistic_kanji'),
    path('get_word', views.get_word, name='get_word'),
    path('save_kanji_score', views.save_kanji_score, name='save_kanji_score'),
    path('load_excel_file', views.load_excel_file, name='load_excel_file'),
    path('get_list_remain_word', views.get_list_remain_word, name='get_list_remain_word'),
    path('chia_group', views.divide_group, name='chia_group'),
]