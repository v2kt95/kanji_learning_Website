from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # path('get_word', views.get_word, name='get_word'),
    path('get_word2', views.getWorsd2, name='get_word2'),
    path('reset', views.reset, name='reset'),
    path('mark_word', views.mark_word, name='mark_word'),
    path('load_excel_file', views.load_excel_file, name='load_excel_file'),
    path('get_list_remain_word', views.get_list_remain_word, name='get_list_remain_word'),
    path('get_list_done_word', views.get_list_done_word, name='get_list_done_word'),
    path('get_list_old_word', views.get_list_old_word, name='get_list_old_word'),
]