from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('get_word', views.get_word, name='get_word'),
    path('reset', views.reset, name='reset'),
    path('mark_word', views.mark_word, name='mark_word'),
    path('load_excel_file', views.load_excel_file, name='load_excel_file'),
]