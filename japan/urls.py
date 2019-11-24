from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('get_statistic_kanji', views.get_statistic_kanji, name='get_statistic_kanji'),
    path('get_word2', views.get_word, name='get_word2'),
    path('reset', views.reset, name='reset'),
    path('mark_word', views.mark_word, name='mark_word'),
    path('load_excel_file', views.load_excel_file, name='load_excel_file'),
    path('get_list_remain_word', views.get_list_remain_word, name='get_list_remain_word'),
    path('get_list_done_word', views.get_list_done_word, name='get_list_done_word'),
]