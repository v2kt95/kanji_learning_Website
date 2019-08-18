from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('load_excel_file', views.load_excel_file, name='load_excel_file'),
    path('get_statistic_grammar', views.get_statistic_grammar, name='get_statistic_grammar'),
    path('get_example', views.get_example, name='get_example'),
    path('get_list_done_grammar', views.get_list_done_grammar, name='get_list_done_grammar'),
    path('get_list_remain_grammar', views.get_list_remain_grammar, name='get_list_remain_grammar'),
    path('reset', views.reset, name='reset'),
]