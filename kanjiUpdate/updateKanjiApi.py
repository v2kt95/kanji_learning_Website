# import request
from japan.models import Kanji,Word

def update_kanji():
	kanjis = Kanji.objects.all()
	for kanji in kanjis:
		kanji.remember_point -= kanji.strokes
		kanji.save()
	print("updated kanji...\n")