from django.db import models


# Create your models here.
class Grammar(models.Model):
    N5 = 'N5'
    N4 = 'N4'
    N3 = 'N3'
    N2 = 'N2'
    N1 = 'N1'
    JAPAN_LEVEL = [
        (N5, 'N5'),
        (N4, 'N4'),
        (N3, 'N3'),
        (N2, 'N2'),
        (N1, 'N1'),
    ]
    _formula = models.CharField(max_length=200)
    _vietnam_equivalent = models.CharField(max_length=200)
    _english_equivalent = models.CharField(max_length=200)
    _unit = models.IntegerField(default=0)
    _japan_level = models.CharField(default=N5, choices=JAPAN_LEVEL, max_length=200)
    _level = models.IntegerField(default=1)
    _day_down = models.IntegerField(default=1)
    _day_count = models.IntegerField(default=1)

    @property
    def formula(self):
        return self._formula

    @formula.setter
    def formula(self, value):
        self._formula = value

    @property
    def vietnam_equivalent(self):
        return self._vietnam_equivalent

    @vietnam_equivalent.setter
    def vietnam_equivalent(self, value):
        self._vietnam_equivalent = value

    @property
    def english_equivalent(self):
        return self._english_equivalent

    @english_equivalent.setter
    def english_equivalent(self, value):
        self._english_equivalent = value

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = value

    @property
    def japan_level(self):
        return self._japan_level

    @japan_level.setter
    def japan_level(self, value):
        self._japan_level = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def day_down(self):
        return self._day_down

    @day_down.setter
    def day_down(self, value):
        self._day_down = value

    @property
    def day_count(self):
        return self._day_count

    @day_count.setter
    def day_count(self, value):
        self._day_count = value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.japan_level == self.N5:
            if self.unit <= 12:
                self.day_down = 8
            else:
                self.day_down = 6
        elif self.japan_level == self.N4:
            if self.unit <= 37:
                self.day_down = 4
            else:
                self.day_down = 2
        else:
            self.day_down = 2

    def __str__(self):
        return self.english_equivalent

    @staticmethod
    def get_grammar_by_formula(formula):
        return Grammar.objects.filter(_formula=formula).first()

    @staticmethod
    def get_grammars_by_conditions_and_order(order_by='', **kwargs):
        grammar = Grammar.objects
        for key, value in kwargs.items():
            grammar = grammar.filter(**{"_" + key: value})
        if order_by is not '':
            grammar = grammar.order_by("_" + order_by)
        return grammar

    @staticmethod
    def is_existed_grammar_by_formula(formula):
        return Grammar.objects.filter(_formula=formula).count() > 0

    @staticmethod
    def count_grammar(**kwargs):
        grammar_count = Grammar.objects
        for key, value in kwargs.items():
            grammar_count = grammar_count.filter(**{"_" + key: value})
        return grammar_count.count()

    @staticmethod
    def create(formula, vietnam_equivalent, english_equivalent, unit, japan_level):
        return Grammar(_formula=formula,
                       _vietnam_equivalent=vietnam_equivalent,
                       _english_equivalent=english_equivalent,
                       _unit=unit,
                       _japan_level=japan_level)


class Sentence(models.Model):
    _grammar = models.ForeignKey(Grammar, on_delete=models.CASCADE)
    _content = models.CharField(max_length=200, default="")
    _vietnam_meaning = models.CharField(max_length=200)

    @property
    def grammar(self):
        return self._grammar

    @grammar.setter
    def grammar(self, value):
        self._grammar = value

    @property
    def vietnam_meaning(self):
        return self._vietnam_meaning

    @vietnam_meaning.setter
    def vietnam_meaning(self, value):
        self._vietnam_meaning = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    def __str__(self):
        return self.vietnam_meaning

    @staticmethod
    def is_existed_sentence_by_grammar_and_content(grammar, content):
        return Sentence.objects.filter(_grammar=grammar).filter(_content=content).count() > 0

    @staticmethod
    def create(grammar, content, vietnam_meaning):
        return Sentence(_grammar=grammar,
                        _content=content,
                        _vietnam_meaning=vietnam_meaning)

    @staticmethod
    def get_sentence_by_conditions_and_order(order_by='', **kwargs):
        sentence = Sentence.objects
        for key, value in kwargs.items():
            sentence = sentence.filter(**{"_" + key: value})
        if order_by is not '' and order_by is not '?':
            sentence = sentence.order_by("_" + order_by)
        elif order_by is '?':
            sentence = sentence.order_by(order_by)
        return sentence
