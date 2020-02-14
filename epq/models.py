from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import itertools
import json

author = 'Victor van Pelt'

doc = """
Ex-post Questionnaire
"""


class Constants(BaseConstants):
    name_in_url = 'epq'
    players_per_group = None
    num_rounds = 1
    StandardChoices=[
        [1, 'Disagree strongly'],
        [2, 'Disagree moderately'],
        [3, 'Disagree a little'],
        [4, 'Neither agree nor disagree'],
        [5, 'Agree a little'],
        [6, 'Agree moderately'],
        [7, 'Agree strongly'],
    ]

class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            dict = p.participant.vars
            if 'supervisor' not in dict:
                if 'manager' not in dict:
                    p.participant.vars['supervisor'] = 1
                    p.participant.vars['manager'] = 1
                else:
                    pass
            else:
                pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    #Introduction
    # accept_info = models.BooleanField(blank=False, widget=widgets.CheckboxInput)

    #Survey1
    fun1 = models.IntegerField(
        label="I participated seriously in the study.",
        choices=Constants.StandardChoices
    )
    fun2 = models.IntegerField(
        label="I thought well about my choices before making any decisions.",
        choices=Constants.StandardChoices
    )
    fun3 = models.IntegerField(
        label="I really cared about the outcomes of my decisions.",
        choices=Constants.StandardChoices
    )
    fun4 = models.IntegerField(
        label="I got more and more involved as the study progressed.",
        choices=Constants.StandardChoices
    )
    fun5 = models.IntegerField(
        label="I started to loose my interest as the study progressed.",
        choices=Constants.StandardChoices
    )
    info_diff = models.IntegerField(
        label="The procedure that supervisors have to go through to get access to information about the individual investments was difficult to understand.",
        choices=Constants.StandardChoices
    )

    #Survey 2 (supervisor last) (Managers last)
    sup1 = models.IntegerField(
        label="In general I was curious about the separate investments of the two BU managers.",
        choices=Constants.StandardChoices
    )
    sup2 = models.IntegerField(
        label="In general, I wanted to know whether one BU manager had invested more than the other.",
        choices=Constants.StandardChoices
    )
    sup3 = models.IntegerField(
        label="I wanted to reward BU managers who acted cooperatively.",
        choices=Constants.StandardChoices
    )
    sup4 = models.IntegerField(
        label="I wanted to punish BU managers who did not act cooperatively.",
        choices=Constants.StandardChoices
    )
    sup5 = models.IntegerField(
        label="I thought BU managers who made small investments acted unfairly.",
        choices=Constants.StandardChoices
    )
    sup6 = models.IntegerField(
        label="I thought it was important that BU managers who tried to get more than their fair share got punished.",
        choices=Constants.StandardChoices
    )
    sup7 = models.IntegerField(
        label="I thought it was important that BU managers who acted in the common interest got rewarded.",
        choices=Constants.StandardChoices
    )
    sup8 = models.IntegerField(
        label="I thought it was important that BU managers who acted in the common interest got at least a fair return.",
        choices=Constants.StandardChoices
    )
    sup9 = models.IntegerField(
        label="I wanted to teach the BU managers a lesson that they should cooperate with each other.",
        choices=Constants.StandardChoices
    )
    sup10 = models.IntegerField(
        label="I wanted to teach the BU managers a lesson that small investments are unacceptable.",
        choices=Constants.StandardChoices
    )

    #Survey 3 (supervisor last) (managers last)
    sup11 = models.IntegerField(
        label="I wanted to repay the trust that BU managers placed in me by investing part of their base amount.",
        choices=Constants.StandardChoices
    )
    sup12 = models.IntegerField(
        label="I wanted to reward those BU managers who expected me to be a fair supervisor.",
        choices=Constants.StandardChoices
    )
    sup13 = models.IntegerField(
        label="I wanted to punish those BU managers who did not expect me to be a fair supervisor.",
        choices=Constants.StandardChoices
    )
    sup14 = models.IntegerField(
        label="I did not want to disappoint BU managers who trusted me to reward high investments.",
        choices=Constants.StandardChoices
    )
    sup15 = models.IntegerField(
        label="I wanted to show that I am a trustworthy person.",
        choices=Constants.StandardChoices
    )
    sup16 = models.IntegerField(
        label="My offers for the information depended on the total investment of the two BU managers.",
        choices=Constants.StandardChoices
    )
    sup17 = models.IntegerField(
        label="My offers for the information depended on the number of combinations of individual investments that could have led to the total investment.",
        choices=Constants.StandardChoices
    )
    sup18 = models.IntegerField(
        label="I was likely to offer a higher price for the information if there was a bigger chance that one of the BU managers had invested much more than the other.",
        choices=Constants.StandardChoices
    )

    #Survey 4  (supervisors last) (managers last) (managers always)
    man1 = models.IntegerField(
        label="I felt it was my duty to make high investments.",
        choices=Constants.StandardChoices
    )
    man2 = models.IntegerField(
        label="I felt that not making high investments was uncooperative.",
        choices=Constants.StandardChoices
    )
    man3 = models.IntegerField(
        label="I felt that making high investments was the fair thing to do.",
        choices=Constants.StandardChoices
    )
    man4 = models.IntegerField(
        label="I felt that not making high investments was unfair to the other BU manager.",
        choices=Constants.StandardChoices
    )
    man5 = models.IntegerField(
        label="I felt that not making high investments was unfair towards the supervisor.",
        choices=Constants.StandardChoices
    )
    man6 = models.IntegerField(
        label="In general, I trusted the supervisors to give me a fair reward.",
        choices=Constants.StandardChoices
    )
    man7 = models.IntegerField(
        label="My trust in the supervisors increased during the study.",
        choices=Constants.StandardChoices
    )
    man8 = models.IntegerField(
        label="My trust in the other BU managers increased during the study.",
        choices=Constants.StandardChoices
    )
    man9 = models.IntegerField(
        label="My trust in the supervisors decreased during the study.",
        choices=Constants.StandardChoices
    )
    man10 = models.IntegerField(
        label="My trust in the other BU managers decreased during the study.",
        choices=Constants.StandardChoices
    )
    man11 = models.IntegerField(
        label="I felt I was sometimes treated unfairly by the supervisor.",
        choices=Constants.StandardChoices
    )
    man12 = models.IntegerField(
        label="I felt I was sometimes treated unfairly by the other BU manager.",
        choices=Constants.StandardChoices
    )

    #Survey 5
    trust1 = models.IntegerField(
        label="I trust others.",
        choices=Constants.StandardChoices
    )
    trust2 = models.IntegerField(
        label="I trust what other people say.",
        choices=Constants.StandardChoices
    )
    trust3 = models.IntegerField(
        label="I am wary of others.",
        choices=Constants.StandardChoices
    )
    trust4 = models.IntegerField(
        label="I suspect hidden motives in others.",
        choices=Constants.StandardChoices
    )
    trust5 = models.IntegerField(
        label="I distrust people.",
        choices=Constants.StandardChoices
    )
    trust6 = models.IntegerField(
        label="I would never cheat on my taxes.",
        choices=Constants.StandardChoices
    )
    trust7 = models.IntegerField(
        label="I turn my back on others.",
        choices=Constants.StandardChoices
    )
    trust8 = models.IntegerField(
        label="I act at the expense of others.",
        choices=Constants.StandardChoices
    )
    trust9 = models.IntegerField(
        label="I respect the privacy of others.",
        choices=Constants.StandardChoices
    )
    trust10 = models.IntegerField(
        label="I respect authority.",
        choices=Constants.StandardChoices
    )

    #Survey 6
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
            [7, 'I prefer not to say']
        ]
    )

    educational_level = models.IntegerField(
        label = "What best describes your current educational level?",
        choices = [
            [1, 'Bachelor degree'],
            [2, 'Master degree'],
            [3, 'Other'],
            [4, 'I prefer not to say']
        ]
    )
    educational_track = models.IntegerField(
        label = "What best describes your current educational track?",
        choices = [
            [1, 'Economics'],
            [2, 'Business administration'],
            [3, 'Behavioral sciences'],
            [4, 'Humanities'],
            [5, 'Law'],
            [6, 'Other'],
            [7, 'I prefer not to say']
        ]
    )

    workexperience = models.IntegerField(
        label="Please indicate your work experience. All jobs count, including part-time and volunteer work.",
        blank=False,
        choices=[
            [1, 'I do not have work experience.'],
            [2, 'Less than 5 years work experience.'],
            [3, '5 to 10 years of work experience'],
            [4, '10 to 20 years work experience.'],
            [5, '20 to 30 years work experience.'],
            [6, '30 to 40 years work experience.'],
            [7, '40 years or more work experience.']
        ]
    )

    english = models.IntegerField(
        label="Please rate your English on a percentage scale between 0 and 100.",
        min=0,
        max=100,
        blank=False,
        initial=None
    )

    gender = models.IntegerField(
        label="Please select your gender.",
        blank=False,
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, 'Other'],
        ]
    )
    age = models.IntegerField(label="Please enter your age.", min=14, max=90, blank=False)