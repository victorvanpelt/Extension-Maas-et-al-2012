import random

from otree.api import *

from . import models


doc = """
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""


class C(BaseConstants):
    NAME_IN_URL = 'payment_info'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass
    # def creating_session(self):
    #     # Ticketnumber
    #     for p in self.get_players(self):
    #         self.tn = self.participant.vars['tn']


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
    # tn = models.IntegerField(min=0, max=999999)


# FUNCTIONS
# PAGES
class PaymentInfo(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'redemption_code': player.participant.label or player.participant.code,
            'eur': player.participant.payoff_plus_participation_fee(),
        }


page_sequence = [PaymentInfo]
