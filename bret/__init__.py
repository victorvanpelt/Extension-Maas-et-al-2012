from __future__ import division

import random

from otree.api import *
from otree.currency import safe_json

# from otree.common import Currency as cu, currency_range, safe_json

# from . import models
# from .config import Constants as C


author = 'Felix Holzmeister & Armin Pfurtscheller'
doc = """
Bomb Risk Elicitation Task (BRET) à la Crosetto/Filippin (2013), Journal of Risk and Uncertainty (47): 31-65.
"""


# ******************************************************************************************************************** #
# *** CLASS CONSTANTS *** #
# ******************************************************************************************************************** #
class C(BaseConstants):

    # oTree Constants
    NAME_IN_URL = 'bret'
    PLAYERS_PER_GROUP = None

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Overall Settings and Appearance --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # value of single collected box
    # if the bomb is not collected, player's payoff per round is determined by <box_value> times <boxes_collected>
    # note that the currency of any earnings is determined by the oTree settings in settings.py
    # if you set this to a decimal number, you must set POINTS_DECIMAL_PLACES in settings.py
    box_value = 0.10
    box_value_eur = 0.10 * 0.50

    # number of rows and columns
    # i.e. the total number of boxes is determined by <num_rows> times <num_cols>
    num_rows = 10
    num_cols = 10

    # box height and box width in pixels
    # make sure that the size of the boxes fits the screen of the device
    # note that the layout is responsive, i.e. boxes will break into new rows if they don't fit
    box_height = '50px'
    box_width = '50px'

    # number of rounds to be played
    NUM_ROUNDS = 1

    # determines whether all rounds played are payed-off or whether one round is randomly chosen for payment
    # if <random_payoff = True>, one round is randomly determined for payment
    # if <random_payoff = False>, the final payoff of the task is the sum of all rounds played
    # note that this is only of interest for the case of <num_rounds> larger than 1
    random_payoff = True

    # if <instructions = True>, a separate template "Instructions.html" is rendered prior to the task in round 1
    # if <instructions = False>, the task starts immediately (e.g. in case of printed instructions)
    instructions = True

    # show feedback by resolving boxes, i.e. toggle boxes and show whether bomb was collected or not
    # if <feedback = True>, the button "Solve" will be rendered and active after game play ends ("Stop")
    # if <feedback = False>, the button "Solve" won't be rendered such that no feedback about game outcome is provided
    feedback = True

    # show results page summarizing the game outcome
    # if <results = True>, a separate page containing all relevant information is displayed after finishing the task
    # if <num_rounds> larger than 1, results are summarized in a table and only shown after all rounds have been played
    results = True


    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Settings Determining Game Play --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # "dynamic" or "static" game play
    # if <dynamic = True>, one box per time interval is collected automatically
    # in case of <dynamic = True>, game play is affected by the variables <time_interval> and <random> below
    # if <dynamic = False>, subjects collect as many boxes as they want by clicking or entering the respective number
    # in case of <dynamic = False>, game play is affected by the variables <random>, <devils_game> and <undoable>
    dynamic = False

    # time interval between single boxes being collected (in seconds)
    # note that this only affects game play if <dynamic = True>
    time_interval = 1.00

    # collect boxes randomly or systematically
    # if <random = False>, boxes are collected row-wise one-by-one, starting in the top-left corner
    # if <random = True>, boxes are collected randomly (Fisher-Yates Algorithm)
    # note that this affects game play in both cases, <dynamic = True> and <dynamic = False>
    random = True

    # determines whether static game play allows for selecting boxes by clicking or by entering a number
    # if <devils_game = True>, game play is similar to Slovic (1965), i.e. boxes are collected by subjects
    # if <devils_game = False>, subjects enter the number of boxes they want to collect
    # note that this only affects game play if <dynamic = False>
    devils_game = False

    # determine whether boxes can be toggled only once or as often as clicked
    # if <undoable = True> boxes can be selected and de-selected indefinitely often
    # if <undoable = False> boxes can be selected only once (i.e. decisions can not be undone)
    # note that this only affects game play if <dynamic = False> and <devils_game = True>
    undoable = True



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
    # Accept the conditions to participate
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


# FUNCTIONS
def set_payoff(player: Player):
    # determine round_result as (potential) payoff per round
    if player.bomb:
        player.round_result = 0
    else:
        player.round_result = player.boxes_collected * C.box_value
    # set payoffs if <random_payoff = True> to round_result of randomly chosen round
    # randomly determine round to pay on player level
    if player.subsession.round_number == 1:
        player.participant.vars['round_to_pay'] = random.randint(1, C.NUM_ROUNDS)
    if C.random_payoff:
        if player.subsession.round_number == player.participant.vars['round_to_pay']:
            player.pay_this_round = True
            player.payoff = cu(player.round_result)
            player.payoff_for_results = round(player.round_result, 2)
            player.payoff_for_results_eur = round(
                player.round_result
                * player.session.config['real_world_currency_per_point'],
                2,
            )
        else:
            player.pay_this_round = False
            player.payoff = cu(0)
            player.payoff_for_results = 0
            player.payoff_for_results_eur = 0
    # set payoffs to round_result if <random_payoff = False>
    else:
        player.payoff = cu(player.round_result)
        player.payoff_for_results = round(player.round_result, 2)
        player.payoff_for_results_eur = round(player.round_result * C.box_value_eur, 2)


# PAGES
# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):
    form_model = 'player'
    form_fields = ['accept_conditions']
    # only display instruction in round 1
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

    # variables for use in template
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'num_rows': C.num_rows,
            'num_cols': C.num_cols,
            'num_boxes': C.num_rows * C.num_cols,
            'num_nobomb': C.num_rows * C.num_cols - 1,
            'box_value': C.box_value,
            'time_interval': C.time_interval,
            'box_value_eur': C.box_value_eur,
        }


# ******************************************************************************************************************** #
# *** CLASS BOMB RISK ELICITATION TASK *** #
# ******************************************************************************************************************** #
class Decision(Page):
    # form fields on player level
    form_model = 'player'
    form_fields = [
        'bomb',
        'boxes_collected',
        'bomb_row',
        'bomb_col',
    ]
    # jsonify BRET settings for Javascript application
    @staticmethod
    def vars_for_template(player: Player):
        reset = player.participant.vars.get('reset', False)
        if reset == True:
            del player.participant.vars['reset']
        input = not C.devils_game if not C.dynamic else False
        otree_vars = {
            'reset': reset,
            'input': input,
            'random': C.random,
            'dynamic': C.dynamic,
            'num_rows': C.num_rows,
            'num_cols': C.num_cols,
            'feedback': C.feedback,
            'undoable': C.undoable,
            'box_width': C.box_width,
            'box_height': C.box_height,
            'time_interval': C.time_interval,
        }
        return {'otree_vars': safe_json(otree_vars)}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['reset'] = True
        set_payoff(player)


# ******************************************************************************************************************** #
# *** CLASS RESULTS *** #
# ******************************************************************************************************************** #
class Results(Page):
    # only display results after all rounds have been played
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == C.NUM_ROUNDS

    # variables for use in template
    @staticmethod
    def vars_for_template(player: Player):
        total_payoff = sum([p.payoff for p in player.in_all_rounds()])
        player.participant.vars['bret_payoff'] = total_payoff
        return {
            'player_in_all_rounds': player.in_all_rounds(),
            'box_value': C.box_value,
            'boxes_total': C.num_rows * C.num_cols,
            'boxes_collected': player.boxes_collected,
            'bomb': player.bomb,
            'bomb_row': player.bomb_row,
            'bomb_col': player.bomb_col,
            'round_result': player.round_result,
            'round_to_pay': player.participant.vars['round_to_pay'],
            'payoff': player.payoff_for_results,
            'total_payoff': total_payoff,
            'payoff_eur': player.payoff_for_results_eur,
        }


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Decision]
if C.instructions == True:
    page_sequence.insert(0, Instructions)
if C.results == True:
    page_sequence.append(Results)
