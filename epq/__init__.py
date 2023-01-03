import itertools
import json
import random

from otree.api import *


author = 'Victor van Pelt'
doc = """
Ex-post Questionnaire
"""


class C(BaseConstants):
    NAME_IN_URL = 'epq'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    STANDARDCHOICES = [
        [1, 'Disagree strongly'],
        [2, 'Disagree moderately'],
        [3, 'Disagree a little'],
        [4, 'Neither agree nor disagree'],
        [5, 'Agree a little'],
        [6, 'Agree moderately'],
        [7, 'Agree strongly'],
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Introduction
    # accept_info = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    # Survey1
    fun1 = models.IntegerField(
        label="I participated seriously in the study.", choices=C.STANDARDCHOICES
    )
    fun2 = models.IntegerField(
        label="I thought well about my choices before making any decisions.",
        choices=C.STANDARDCHOICES,
    )
    fun3 = models.IntegerField(
        label="I really cared about the outcomes of my decisions.",
        choices=C.STANDARDCHOICES,
    )
    fun4 = models.IntegerField(
        label="I got more and more involved as the study progressed.",
        choices=C.STANDARDCHOICES,
    )
    fun5 = models.IntegerField(
        label="I started to lose my interest as the study progressed.",
        choices=C.STANDARDCHOICES,
    )
    info_diff = models.IntegerField(
        label="The procedure that supervisors have to go through to get access to information about the individual investments was difficult to understand.",
        choices=C.STANDARDCHOICES,
    )
    # Survey 2 (supervisor last) (Managers last)
    sup1 = models.IntegerField(
        label="In general I was curious about the separate investments of the two BU managers.",
        choices=C.STANDARDCHOICES,
    )
    sup2 = models.IntegerField(
        label="In general, I wanted to know whether one BU manager had invested more than the other.",
        choices=C.STANDARDCHOICES,
    )
    sup3 = models.IntegerField(
        label="I wanted to reward BU managers who acted cooperatively.",
        choices=C.STANDARDCHOICES,
    )
    sup4 = models.IntegerField(
        label="I wanted to punish BU managers who did not act cooperatively.",
        choices=C.STANDARDCHOICES,
    )
    sup5 = models.IntegerField(
        label="I thought BU managers who made small investments acted unfairly.",
        choices=C.STANDARDCHOICES,
    )
    sup6 = models.IntegerField(
        label="I thought it was important that BU managers who tried to get more than their fair share got punished.",
        choices=C.STANDARDCHOICES,
    )
    sup7 = models.IntegerField(
        label="I thought it was important that BU managers who acted in the common interest got rewarded.",
        choices=C.STANDARDCHOICES,
    )
    sup8 = models.IntegerField(
        label="I thought it was important that BU managers who acted in the common interest got at least a fair return.",
        choices=C.STANDARDCHOICES,
    )
    sup9 = models.IntegerField(
        label="I wanted to teach the BU managers a lesson that they should cooperate with each other.",
        choices=C.STANDARDCHOICES,
    )
    sup10 = models.IntegerField(
        label="I wanted to teach the BU managers a lesson that small investments are unacceptable.",
        choices=C.STANDARDCHOICES,
    )
    # Survey 3 (supervisor last) (managers last)
    sup11 = models.IntegerField(
        label="I wanted to repay the trust that BU managers placed in me by investing part of their base amount.",
        choices=C.STANDARDCHOICES,
    )
    sup12 = models.IntegerField(
        label="I wanted to reward those BU managers who expected me to be a fair supervisor.",
        choices=C.STANDARDCHOICES,
    )
    sup13 = models.IntegerField(
        label="I wanted to punish those BU managers who did not expect me to be a fair supervisor.",
        choices=C.STANDARDCHOICES,
    )
    sup14 = models.IntegerField(
        label="I did not want to disappoint BU managers who trusted me to reward high investments.",
        choices=C.STANDARDCHOICES,
    )
    sup15 = models.IntegerField(
        label="I wanted to show that I am a trustworthy person.", choices=C.STANDARDCHOICES
    )
    sup16 = models.IntegerField(
        label="My offers for the information depended on the total investment of the two BU managers.",
        choices=C.STANDARDCHOICES,
    )
    sup17 = models.IntegerField(
        label="My offers for the information depended on the number of combinations of individual investments that could have led to the total investment.",
        choices=C.STANDARDCHOICES,
    )
    sup18 = models.IntegerField(
        label="I was likely to offer a higher price for the information if there was a bigger chance that one of the BU managers had invested much more than the other.",
        choices=C.STANDARDCHOICES,
    )
    # Survey 4  (supervisors last) (managers last) (managers always)
    man1 = models.IntegerField(
        label="I felt it was my duty to make high investments.", choices=C.STANDARDCHOICES
    )
    man2 = models.IntegerField(
        label="I felt that not making high investments was uncooperative.",
        choices=C.STANDARDCHOICES,
    )
    man3 = models.IntegerField(
        label="I felt that making high investments was the fair thing to do.",
        choices=C.STANDARDCHOICES,
    )
    man4 = models.IntegerField(
        label="I felt that not making high investments was unfair to the other BU manager.",
        choices=C.STANDARDCHOICES,
    )
    man5 = models.IntegerField(
        label="I felt that not making high investments was unfair towards the supervisor.",
        choices=C.STANDARDCHOICES,
    )
    man6 = models.IntegerField(
        label="In general, I trusted the supervisors to give me a fair reward.",
        choices=C.STANDARDCHOICES,
    )
    man7 = models.IntegerField(
        label="My trust in the supervisors increased during the study.",
        choices=C.STANDARDCHOICES,
    )
    man8 = models.IntegerField(
        label="My trust in the other BU managers increased during the study.",
        choices=C.STANDARDCHOICES,
    )
    man9 = models.IntegerField(
        label="My trust in the supervisors decreased during the study.",
        choices=C.STANDARDCHOICES,
    )
    man10 = models.IntegerField(
        label="My trust in the other BU managers decreased during the study.",
        choices=C.STANDARDCHOICES,
    )
    man11 = models.IntegerField(
        label="I felt I was sometimes treated unfairly by the supervisor.",
        choices=C.STANDARDCHOICES,
    )
    man12 = models.IntegerField(
        label="I felt I was sometimes treated unfairly by the other BU manager.",
        choices=C.STANDARDCHOICES,
    )
    # Survey 5
    trust1 = models.IntegerField(label="I trust others.", choices=C.STANDARDCHOICES)
    trust2 = models.IntegerField(
        label="I trust what other people say.", choices=C.STANDARDCHOICES
    )
    trust3 = models.IntegerField(label="I am wary of others.", choices=C.STANDARDCHOICES)
    trust4 = models.IntegerField(
        label="I suspect hidden motives in others.", choices=C.STANDARDCHOICES
    )
    trust5 = models.IntegerField(label="I distrust people.", choices=C.STANDARDCHOICES)
    trust6 = models.IntegerField(
        label="I would never cheat on my taxes.", choices=C.STANDARDCHOICES
    )
    trust7 = models.IntegerField(
        label="I turn my back on others.", choices=C.STANDARDCHOICES
    )
    trust8 = models.IntegerField(
        label="I act at the expense of others.", choices=C.STANDARDCHOICES
    )
    trust9 = models.IntegerField(
        label="I respect the privacy of others.", choices=C.STANDARDCHOICES
    )
    trust10 = models.IntegerField(label="I respect authority.", choices=C.STANDARDCHOICES)
    # Survey 6
    nationality = models.IntegerField(
        label="Please select your region of residence.",
        blank=False,
        choices=[
            [1, 'North-America'],
            [2, 'Central and South-America'],
            [3, 'Asia'],
            [4, 'Europe'],
            [5, 'Australia and Oceania'],
            [6, 'Africa'],
            [7, 'I prefer not to say'],
        ],
    )
    educational_level = models.IntegerField(
        label="What best describes your current educational level?",
        choices=[
            [1, 'Bachelor degree'],
            [2, 'Master degree'],
            [3, 'Other'],
            [4, 'I prefer not to say'],
        ],
    )
    educational_track = models.IntegerField(
        label="What best describes your current educational track?",
        choices=[
            [1, 'Economics'],
            [2, 'Business administration'],
            [3, 'Behavioral sciences'],
            [4, 'Humanities'],
            [5, 'Law'],
            [6, 'Other'],
            [7, 'I prefer not to say'],
        ],
    )
    workexperience = models.IntegerField(
        label="Please indicate your work experience. All jobs count, including part-time and volunteer work.",
        blank=False,
        choices=[
            [1, 'I do not have work experience.'],
            [2, 'Less than 5 years of work experience.'],
            [3, '5 to 10 years of work experience.'],
            [4, '10 to 20 years work experience.'],
            [5, '20 to 30 years work experience.'],
            [6, '30 to 40 years work experience.'],
            [7, '40 years or more work experience.'],
        ],
    )
    english = models.IntegerField(
        label="Please rate your English on a percentage scale between 0 and 100.",
        min=0,
        max=100,
        blank=False,
        initial=None,
    )
    gender = models.IntegerField(
        label="Please select your gender.",
        blank=False,
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, 'Other'],
        ],
    )
    age = models.IntegerField(label="Please enter your age.", min=14, max=90, blank=False)


# FUNCTIONS
def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        dict = p.participant.vars
        if 'supervisor' not in dict:
            if 'manager' not in dict:
                p.participant.vars['supervisor'] = 1
                p.participant.vars['manager'] = 1
            else:
                pass
        else:
            pass


# PAGES
class Introduction(Page):
    pass
    # form_model = 'player'
    # form_fields = ['accept_info']


class Survey1(Page):
    form_model = 'player'
    form_fields = ['fun1', 'fun2', 'fun3', 'fun4', 'fun5', 'info_diff']

    @staticmethod
    def get_form_fields(player: Player):
        fields = ['fun1', 'fun2', 'fun3', 'fun4', 'fun5', 'info_diff']
        random.shuffle(fields)
        return fields


class Survey2(Page):
    form_model = 'player'
    form_fields = ['sup1', 'sup2', 'sup3', 'sup4', 'sup5', 'sup6', 'sup7', 'sup8', 'sup9', 'sup10']

    @staticmethod
    def get_form_fields(player: Player):
        fields = ['sup1', 'sup2', 'sup3', 'sup4', 'sup5', 'sup6', 'sup7', 'sup8', 'sup9', 'sup10']
        random.shuffle(fields)
        return fields

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['supervisor'] == 1


class Survey3(Page):
    form_model = 'player'
    form_fields = ['sup11', 'sup12', 'sup13', 'sup14', 'sup15', 'sup16', 'sup17', 'sup18']

    @staticmethod
    def get_form_fields(player: Player):
        fields = ['sup11', 'sup12', 'sup13', 'sup14', 'sup15', 'sup16', 'sup17', 'sup18']
        random.shuffle(fields)
        return fields

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['supervisor'] == 1


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
        'man12',
    ]

    @staticmethod
    def get_form_fields(player: Player):
        fields = [
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
            'man12',
        ]
        random.shuffle(fields)
        return fields

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['manager'] == 1


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
        'trust10',
    ]

    @staticmethod
    def get_form_fields(player: Player):
        fields = [
            'trust1',
            'trust2',
            'trust3',
            'trust4',
            'trust5',
            'trust6',
            'trust7',
            'trust8',
            'trust9',
            'trust10',
        ]
        random.shuffle(fields)
        return fields


class Survey6(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'nationality',
        'educational_level',
        'educational_track',
        'workexperience',
        'english',
    ]

    @staticmethod
    def get_form_fields(player: Player):
        fields = [
            'age',
            'gender',
            'nationality',
            'educational_level',
            'educational_track',
            'workexperience',
            'english',
        ]
        random.shuffle(fields)
        return fields


page_sequence = [Introduction, Survey1, Survey2, Survey3, Survey4, Survey5, Survey6]
tot_pages = len(page_sequence) - 1
