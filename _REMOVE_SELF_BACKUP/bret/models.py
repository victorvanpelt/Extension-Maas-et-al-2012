from otree.api import (
    models, widgets, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from .config import Constants

author = 'Felix Holzmeister & Armin Pfurtscheller'

doc = """
Bomb Risk Elicitation Task (BRET) à la Crosetto/Filippin (2013), Journal of Risk and Uncertainty (47): 31-65.
"""


# ******************************************************************************************************************** #
# *** CLASS SUBSESSION *** #
# ******************************************************************************************************************** #
class Subsession(BaseSubsession):
    pass

# ******************************************************************************************************************** #
# *** CLASS GROUP *** #
# ******************************************************************************************************************** #
class Group(BaseGroup):
    pass


# ******************************************************************************************************************** #
# *** CLASS PLAYER *** #
# ******************************************************************************************************************** #
class Player(BasePlayer):

    #Accept the conditions to participate
    accept_conditions = models.BooleanField(blank=False, widget=widgets.CheckboxInput)

    # whether bomb is collected or not
    # store as integer because it's easier for interop with JS
    bomb = models.IntegerField()

    # location of bomb
    bomb_row = models.PositiveIntegerField()
    bomb_col = models.PositiveIntegerField()

    # number of collected boxes
    boxes_collected = models.IntegerField()

    # --- set round results and player's payoff
    # ------------------------------------------------------------------------------------------------------------------
    pay_this_round = models.BooleanField()
    round_result = models.FloatField()
    payoff_for_results = models.FloatField()
    payoff_for_results_eur = models.FloatField()

    def set_payoff(self):

        # determine round_result as (potential) payoff per round
        if self.bomb:
            self.round_result = 0
        else:
            self.round_result = self.boxes_collected * C.BOX_VALUE

        # set payoffs if <random_payoff = True> to round_result of randomly chosen round
        # randomly determine round to pay on player level
        if self.subsession.round_number == 1:
            self.participant.vars['round_to_pay'] = random.randint(1,C.NUM_ROUNDS)

        if C.RANDOM_PAYOFF:
            if self.subsession.round_number == self.participant.vars['round_to_pay']:
                self.pay_this_round = True
                self.payoff = c(self.round_result)
                self.payoff_for_results = round(self.round_result, 2)
                self.payoff_for_results_eur = round(self.round_result * settings.SESSION_CONFIG_DEFAULTS['real_world_currency_per_point'], 2)
            else:
                self.pay_this_round = False
                self.payoff = c(0)
                self.payoff_for_results = 0
                self.payoff_for_results_eur = 0

        # set payoffs to round_result if <random_payoff = False>
        else:
            self.payoff = c(self.round_result)
            self.payoff_for_results = round(self.round_result, 2)
            self.payoff_for_results_eur = round(self.round_result * C.BOX_VALUE_EUR, 2)
