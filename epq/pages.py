from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
import json

class Introduction(Page):
    pass
    # form_model = 'player'
    # form_fields = ['accept_info']

class Survey1(Page):
    form_model = 'player'
    form_fields = [
        'fun1',
        'fun2',
        'fun3',
        'fun4',
        'fun5',
        'info_diff'
    ]

    def get_form_fields(self):
        fields = self.form_fields
        random.shuffle(fields)
        return fields

class Survey2(Page):
    form_model = 'player'
    form_fields = [
        'sup1',
        'sup2',
        'sup3',
        'sup4',
        'sup5',
        'sup6',
        'sup7',
        'sup8',
        'sup9',
        'sup10'
    ]

    def get_form_fields(self):
        fields = self.form_fields
        random.shuffle(fields)
        return fields

    def is_displayed(self):
        return self.participant.vars['supervisor'] == 1

class Survey3(Page):
    form_model = 'player'
    form_fields = [
        'sup11',
        'sup12',
        'sup13',
        'sup14',
        'sup15',
        'sup16',
        'sup17',
        'sup18'
    ]

    def get_form_fields(self):
        fields = self.form_fields
        random.shuffle(fields)
        return fields

    def is_displayed(self):
        return self.participant.vars['supervisor'] == 1

class Survey4(Page):
    form_model = 'player'
    form_fields = [
        'man1',
        'man2',
        'man3',
        'man4',
        'man5',
        'man6',
        'man7',
        'man8',
        'man9',
        'man10',
        'man11',
        'man12'
    ]

    def get_form_fields(self):
        fields = self.form_fields
        random.shuffle(fields)
        return fields

    def is_displayed(self):
        return self.participant.vars['manager'] == 1

class Survey5(Page):
    form_model = 'player'
    form_fields = [
        'trust1',
        'trust2',
        'trust3',
        'trust4',
        'trust5',
        'trust6',
        'trust7',
        'trust8',
        'trust9',
        'trust10'
    ]

    def get_form_fields(self):
        fields = self.form_fields
        random.shuffle(fields)
        return fields

class Survey5(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'nationality',
        'educational_level',
        'educational_track',
        'workexperience',
        'english'
    ]

    def get_form_fields(self):
        fields = self.form_fields
        random.shuffle(fields)
        return fields

page_sequence = [
    Introduction,
    Survey1,
    Survey2,
    Survey3,
    Survey4,
    Survey5
]

tot_pages = len(page_sequence)-1