# import request
from japan.models import Kanji,Word

def update_kanji():
	kanjis = Kanji.objects.get(id=153)
	kanjis.remember_point -= kanji.strokes
	kanjis.save()
	# for kanji in kanjis:
	# 	kanji.remember_point -= kanji.strokes
	# 	kanji.save()
	print("updated kanji...\n")